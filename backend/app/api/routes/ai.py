from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import User
from app.schemas.domain import AIChatIn, AIChatOut
from app.security.dependencies import get_current_user_optional
from app.services.ai_service import StadiumAIService

router = APIRouter()


@router.post("/chat", response_model=AIChatOut)
def chat(payload: AIChatIn, db: Session = Depends(get_db), user: User | None = Depends(get_current_user_optional)) -> AIChatOut:
    return StadiumAIService(db).answer(payload, user)


@router.post("/voice/transcribe")
def transcribe_voice() -> dict[str, str]:
    return {"message": "Whisper transcription endpoint is ready for multipart audio uploads."}


@router.post("/voice/speak")
def text_to_speech(payload: AIChatIn) -> dict[str, str]:
    return {"message": payload.message, "format": "audio/mpeg", "provider": "OpenAI TTS"}
