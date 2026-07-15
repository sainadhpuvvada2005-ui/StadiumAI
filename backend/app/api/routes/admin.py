from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import AuditLog, Gate, Match, RoleName, User
from app.security.dependencies import require_roles

router = APIRouter()


@router.get("/users")
def users(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0), db: Session = Depends(get_db), user: User = Depends(require_roles(RoleName.admin))):
    records = db.scalars(select(User).limit(limit).offset(offset)).all()
    return [{"id": str(item.id), "email": item.email, "full_name": item.full_name, "role": item.role.name.value, "preferred_language": item.preferred_language, "is_active": item.is_active} for item in records]


@router.get("/matches")
def matches(db: Session = Depends(get_db), user: User = Depends(require_roles(RoleName.admin))):
    records = db.scalars(select(Match).order_by(Match.starts_at)).all()
    return [{"id": str(item.id), "home_team": item.home_team, "away_team": item.away_team, "venue": item.venue, "starts_at": item.starts_at.isoformat(), "status": item.status} for item in records]


@router.get("/gates")
def gates(db: Session = Depends(get_db), user: User = Depends(require_roles(RoleName.admin, RoleName.organizer))):
    records = db.scalars(select(Gate).order_by(Gate.code)).all()
    return [{"id": str(item.id), "code": item.code, "name": item.name, "accessibility": item.accessibility, "current_wait_minutes": item.current_wait_minutes, "congestion_score": item.congestion_score} for item in records]


@router.get("/audit-logs")
def audit_logs(db: Session = Depends(get_db), user: User = Depends(require_roles(RoleName.admin))):
    records = db.scalars(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(200)).all()
    return [{"id": str(item.id), "action": item.action, "entity": item.entity, "entity_id": item.entity_id, "metadata": item.metadata_json, "created_at": item.created_at.isoformat()} for item in records]
