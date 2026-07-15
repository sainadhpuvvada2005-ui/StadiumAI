from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.models.domain import CrowdSnapshot, Energy, Incident, IncidentPriority, IncidentType, Waste, Water
from app.schemas.domain import CrowdInsight, IncidentCreate as IncidentCreateSchema, SustainabilityOut


class CrowdIntelligenceService:
    def __init__(self, db: Session):
        self.db = db

    def insights(self) -> list[CrowdInsight]:
        snapshots = self.db.scalars(select(CrowdSnapshot).order_by(CrowdSnapshot.captured_at.desc()).limit(12)).all()
        insights: list[CrowdInsight] = []
        for item in snapshots:
            risk = "critical" if item.density >= 0.85 or item.wait_minutes >= 25 else "elevated" if item.density >= 0.65 else "normal"
            alt = "Redirect visitors to Gate D and open overflow lanes." if risk != "normal" else "Maintain current routing."
            summary = f"{item.zone} density is {item.density:.0%}; predicted wait is {item.wait_minutes} minutes."
            insights.append(CrowdInsight(zone=item.zone, density=item.density, queue_length=item.queue_length, wait_minutes=item.wait_minutes, risk=risk, ai_summary=summary, alternative_route=alt))
        return insights


class EmergencyCopilotService:
    def __init__(self, db: Session):
        self.db = db

    def create_incident(self, payload: IncidentCreateSchema) -> Incident:
        priority = self._priority(payload.type, payload.description)
        actions = {
            "nearest_response_team": f"{payload.zone} response team",
            "recommended_actions": self._actions(payload.type, priority),
            "evacuation": "Use the nearest accessible exit only if instructed by safety officers.",
        }
        incident = Incident(type=payload.type, zone=payload.zone, description=payload.description, priority=priority, ai_summary=f"{payload.type.value.replace('_', ' ').title()} incident in {payload.zone}. Priority {priority.value}.", recommended_actions=actions)
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return incident

    def _priority(self, incident_type: IncidentType, description: str) -> IncidentPriority:
        text = description.lower()
        if incident_type in {IncidentType.fire, IncidentType.security} or any(word in text for word in ["weapon", "smoke", "unconscious", "stampede"]):
            return IncidentPriority.critical
        if incident_type == IncidentType.medical or "child" in text:
            return IncidentPriority.high
        return IncidentPriority.medium

    def _actions(self, incident_type: IncidentType, priority: IncidentPriority) -> list[str]:
        base = ["Create a geofenced alert for nearby staff", "Keep pedestrian flow away from the response lane"]
        specific = {
            IncidentType.medical: ["Dispatch medical team with AED", "Prepare privacy screen"],
            IncidentType.fire: ["Trigger fire marshal inspection", "Pause ingress near affected zone"],
            IncidentType.security: ["Dispatch security supervisor", "Preserve camera feeds"],
            IncidentType.lost_child: ["Notify family reunification desk", "Share child-safe description with volunteers"],
            IncidentType.operations: ["Assign operations lead", "Monitor queue and utility impact"],
        }
        return specific[incident_type] + base + ([ "Escalate to command center immediately" ] if priority == IncidentPriority.critical else [])


class SustainabilityService:
    def __init__(self, db: Session):
        self.db = db

    def summary(self) -> SustainabilityOut:
        water = float(self.db.scalar(select(func.coalesce(func.sum(Water.liters), 0))) or 0)
        energy = float(self.db.scalar(select(func.coalesce(func.sum(Energy.kwh), 0))) or 0)
        waste = float(self.db.scalar(select(func.coalesce(func.sum(Waste.kilograms), 0))) or 0)
        carbon = energy * 0.39 + waste * 0.18
        recommendations = [
            "Shift concourse lighting to event mode in low-density zones.",
            "Dispatch waste crews to bins with low recycling percentage.",
            "Promote metro exits in AI fan guidance to reduce transport emissions.",
        ]
        return SustainabilityOut(water_liters=water, electricity_kwh=energy, waste_kg=waste, carbon_kg=round(carbon, 2), recommendations=recommendations)
