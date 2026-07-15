from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.models.domain import AIConversation, CrowdSnapshot, FoodCourt, Gate, ParkingLot, TransportOption, User
from app.schemas.domain import AIChatIn, AIChatOut
from typing import Any


class StadiumAIService:
    """RAG-style service boundary. Uses live operational data as retrieved context before generation."""

    def __init__(self, db: Session):
        self.db = db

    def _retrieve_context(self, query: str) -> tuple[list[str], list[str], list[Any]]:
        query_lower = query.lower()
        # Simple keyword-based context selection
        # A more advanced implementation would use embeddings or full-text search.
        gates = self.db.scalars(select(Gate).order_by(Gate.congestion_score.desc()).limit(4)).all() if "gate" in query_lower or "wait" in query_lower else []
        food = self.db.scalars(select(FoodCourt).order_by(FoodCourt.queue_minutes.asc()).limit(3)).all() if "food" in query_lower or "eat" in query_lower else []
        parking = self.db.scalars(select(ParkingLot).order_by(ParkingLot.free_spaces.desc()).limit(3)).all() if "park" in query_lower else []
        transport = self.db.scalars(select(TransportOption).order_by(TransportOption.eta_minutes.asc()).limit(4)).all() if "transport" in query_lower or "bus" in query_lower or "metro" in query_lower else []
        crowd = self.db.scalars(select(CrowdSnapshot).order_by(CrowdSnapshot.captured_at.desc()).limit(6)).all() if "crowd" in query_lower or "busy" in query_lower else []

        # If no specific context is matched, retrieve a general overview.
        if not any([gates, food, parking, transport, crowd]):
            gates = self.db.scalars(select(Gate).order_by(Gate.congestion_score.desc()).limit(2)).all()
            crowd = self.db.scalars(select(CrowdSnapshot).order_by(CrowdSnapshot.captured_at.desc()).limit(2)).all()

        facts = [
            *[f"Gate {g.code}: wait {g.current_wait_minutes} min, congestion {g.congestion_score:.2f}, accessible={g.accessibility}" for g in gates],
            *[f"{f.name}: zone {f.zone}, queue {f.queue_minutes} min, open stalls {f.open_stalls}" for f in food],
            *[f"{p.name}: {p.free_spaces}/{p.total_spaces} spaces free, accessible spaces {p.accessible_spaces}" for p in parking],
            *[f"{t.mode} {t.route_name}: ETA {t.eta_minutes} min, crowd {t.crowd_level:.2f}, carbon {t.carbon_grams}g" for t in transport],
            *[f"{c.zone}: density {c.density:.2f}, queue {c.queue_length}, wait {c.wait_minutes} min" for c in crowd],
        ]
        sources = ["gates", "food_courts", "parking", "transport", "crowd"]
        raw_context = gates + food + parking + transport + crowd
        return facts, sources, raw_context

    def answer(self, payload: AIChatIn, user: User | None) -> AIChatOut:
        facts, sources, raw_context = self._retrieve_context(payload.message)
        answer = self._generate_answer(payload.language, payload.message, facts[:12])
        recommendation = self._derive_recommendation(raw_context)
        self.db.add(AIConversation(user_id=user.id if user else None, language=payload.language, prompt=payload.message, response=answer, sources={"tables": sources}))
        self.db.commit()
        return AIChatOut(answer=answer, language=payload.language, sources=sources, recommendations=[recommendation])

    def _generate_answer(self, language: str, question: str, facts: list[str]) -> str:
        settings = get_settings()
        if settings.openai_api_key:
            from openai import OpenAI

            client = OpenAI(api_key=settings.openai_api_key)
            response = client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "You are STADIUMAI. Answer in the requested language using only supplied live stadium facts. Prioritize safety, accessibility, crowd dispersion, and sustainability."},
                    {"role": "user", "content": f"Language: {language}\nQuestion: {question}\nLive facts:\n" + "\n".join(facts)},
                ],
                temperature=0.2,
            )
            return response.choices[0].message.content or "Live stadium data is available, but no answer was generated."
        return self._compose_grounded_answer(language, facts)

    def _compose_grounded_answer(self, language: str, facts: list[str]) -> str:
        labels = {
            "en": "Based on live stadium data",
            "es": "Segun los datos en vivo del estadio",
            "fr": "Selon les donnees en direct du stade",
            "pt": "Com base nos dados ao vivo do estadio",
            "ar": "استنادا إلى بيانات الاستاد الحية",
            "hi": "लाइव स्टेडियम डेटा के आधार पर",
        }
        lead = labels.get(language, labels["en"])
        context = "; ".join(facts) if facts else "No live records are available yet."
        return f"{lead}: {context}."

    def _derive_recommendation(self, raw_context: list[Any]) -> str:
        congested_gates = [g for g in raw_context if isinstance(g, Gate) and (g.congestion_score >= 0.8 or g.current_wait_minutes >= 20)]
        if congested_gates:
            return f"Reduce pressure around Gate {congested_gates[0].code} by routing fans to the lowest-wait accessible gate."
        return "Maintain current routing and keep monitoring live crowd, transport, and accessibility signals."
