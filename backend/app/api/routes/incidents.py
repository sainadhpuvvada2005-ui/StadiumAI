from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import Incident, RoleName, User
from app.schemas.domain import IncidentCreate, IncidentOut
from app.security.dependencies import require_roles
from app.services.intelligence import EmergencyCopilotService

router = APIRouter()


@router.get("", response_model=list[IncidentOut])
def list_incidents(db: Session = Depends(get_db), user: User = Depends(require_roles(RoleName.volunteer, RoleName.organizer, RoleName.admin))):
    incidents = db.scalars(select(Incident).order_by(Incident.created_at.desc()).limit(100)).all()
    return [IncidentOut(id=str(i.id), type=i.type, zone=i.zone, description=i.description, priority=i.priority, status=i.status, ai_summary=i.ai_summary, recommended_actions=i.recommended_actions, created_at=i.created_at) for i in incidents]


@router.post("", response_model=IncidentOut)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db), user: User = Depends(require_roles(RoleName.volunteer, RoleName.organizer, RoleName.admin))):
    i = EmergencyCopilotService(db).create_incident(payload)
    return IncidentOut(id=str(i.id), type=i.type, zone=i.zone, description=i.description, priority=i.priority, status=i.status, ai_summary=i.ai_summary, recommended_actions=i.recommended_actions, created_at=i.created_at)
