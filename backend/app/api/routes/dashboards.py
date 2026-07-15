from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.domain import FoodCourt, Gate, Incident, Match, ParkingLot, RoleName, Task, Ticket, TransportOption, User, Volunteer
from app.schemas.domain import CrowdInsight, DashboardMetric, SustainabilityOut
from app.security.dependencies import get_current_user, require_roles
from app.services.intelligence import CrowdIntelligenceService, SustainabilityService

router = APIRouter()


@router.get("/fan")
def fan_dashboard(db: Session = Depends(get_db), user: User = Depends(require_roles(RoleName.fan, RoleName.admin))):
    tickets = db.scalars(select(Ticket).where(Ticket.user_id == user.id).limit(10)).all()
    matches = db.scalars(select(Match).order_by(Match.starts_at).limit(5)).all()
    parking = db.scalars(select(ParkingLot).order_by(ParkingLot.free_spaces.desc()).limit(5)).all()
    food = db.scalars(select(FoodCourt).order_by(FoodCourt.queue_minutes).limit(5)).all()
    return {
        "tickets": [{"id": str(t.id), "qr_token": t.qr_token, "match_id": str(t.match_id), "seat_id": str(t.seat_id)} for t in tickets],
        "upcoming_matches": [{"id": str(m.id), "home_team": m.home_team, "away_team": m.away_team, "venue": m.venue, "starts_at": m.starts_at.isoformat(), "status": m.status} for m in matches],
        "parking": [{"name": p.name, "free_spaces": p.free_spaces, "total_spaces": p.total_spaces, "accessible_spaces": p.accessible_spaces} for p in parking],
        "food": [{"name": f.name, "zone": f.zone, "queue_minutes": f.queue_minutes, "open_stalls": f.open_stalls} for f in food],
        "crowd": CrowdIntelligenceService(db).insights(),
    }


@router.get("/volunteer")
def volunteer_dashboard(db: Session = Depends(get_db), user: User = Depends(require_roles(RoleName.volunteer, RoleName.organizer, RoleName.admin))):
    volunteer = db.scalar(select(Volunteer).where(Volunteer.user_id == user.id))
    tasks = db.scalars(select(Task).where(Task.volunteer_id == volunteer.id).limit(20)).all() if volunteer and volunteer.id else []
    return {
        "profile": None if not volunteer else {"id": str(volunteer.id), "assigned_zone": volunteer.assigned_zone, "shift_starts_at": volunteer.shift_starts_at.isoformat(), "shift_ends_at": volunteer.shift_ends_at.isoformat()},
        "tasks": [{"id": str(t.id), "title": t.title, "status": t.status, "priority": t.priority} for t in tasks],
        "alerts": CrowdIntelligenceService(db).insights(),
    }


@router.get("/organizer")
def organizer_dashboard(db: Session = Depends(get_db), user: User = Depends(require_roles(RoleName.organizer, RoleName.admin))):
    metrics = [
        DashboardMetric(label="Active incidents", value=db.scalar(select(func.count()).select_from(Incident)) or 0),
        DashboardMetric(label="Open gates", value=db.scalar(select(func.count()).select_from(Gate)) or 0),
        DashboardMetric(label="Transport routes", value=db.scalar(select(func.count()).select_from(TransportOption)) or 0),
    ]
    return {"metrics": metrics, "crowd": CrowdIntelligenceService(db).insights(), "sustainability": SustainabilityService(db).summary()}


@router.get("/admin")
def admin_dashboard(db: Session = Depends(get_db), user: User = Depends(require_roles(RoleName.admin))):
    return {
        "users": db.scalar(select(func.count()).select_from(User)) or 0,
        "matches": db.scalar(select(func.count()).select_from(Match)) or 0,
        "tickets": db.scalar(select(func.count()).select_from(Ticket)) or 0,
        "system": [DashboardMetric(label="API health", value="online"), DashboardMetric(label="RBAC", value="enabled")],
    }


@router.get("/crowd", response_model=list[CrowdInsight])
def crowd(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return CrowdIntelligenceService(db).insights()


@router.get("/sustainability", response_model=SustainabilityOut)
def sustainability(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return SustainabilityService(db).summary()
