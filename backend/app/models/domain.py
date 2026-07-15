import enum
import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


def uuid_pk() -> Mapped[str]:
    return mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))


class RoleName(str, enum.Enum):
    fan = "fan"
    volunteer = "volunteer"
    organizer = "organizer"
    admin = "admin"


class IncidentType(str, enum.Enum):
    medical = "medical"
    fire = "fire"
    security = "security"
    lost_child = "lost_child"
    operations = "operations"


class IncidentPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[str] = uuid_pk()
    name: Mapped[RoleName] = mapped_column(Enum(RoleName), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(255))


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = uuid_pk()
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(160))
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=True)
    oauth_provider: Mapped[str] = mapped_column(String(40), nullable=True)
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"))
    preferred_language: Mapped[str] = mapped_column(String(8), default="en")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    role: Mapped[Role] = relationship()


class Match(Base):
    __tablename__ = "matches"
    id: Mapped[str] = uuid_pk()
    home_team: Mapped[str] = mapped_column(String(80))
    away_team: Mapped[str] = mapped_column(String(80))
    venue: Mapped[str] = mapped_column(String(120))
    starts_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    status: Mapped[str] = mapped_column(String(40), default="scheduled")


class Gate(Base):
    __tablename__ = "gates"
    id: Mapped[str] = uuid_pk()
    code: Mapped[str] = mapped_column(String(12), unique=True)
    name: Mapped[str] = mapped_column(String(120))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    accessibility: Mapped[bool] = mapped_column(Boolean, default=True)
    current_wait_minutes: Mapped[int] = mapped_column(Integer, default=0)
    congestion_score: Mapped[float] = mapped_column(Float, default=0)


class Seat(Base):
    __tablename__ = "seats"
    id: Mapped[str] = uuid_pk()
    section: Mapped[str] = mapped_column(String(24), index=True)
    row: Mapped[str] = mapped_column(String(12))
    number: Mapped[str] = mapped_column(String(12))
    nearest_gate_id: Mapped[str] = mapped_column(ForeignKey("gates.id"))
    accessible: Mapped[bool] = mapped_column(Boolean, default=False)
    nearest_gate: Mapped[Gate] = relationship()
    __table_args__ = (UniqueConstraint("section", "row", "number", name="seat_unique_label"),)


class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[str] = uuid_pk()
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    match_id: Mapped[str] = mapped_column(ForeignKey("matches.id"))
    seat_id: Mapped[str] = mapped_column(ForeignKey("seats.id"))
    qr_token: Mapped[str] = mapped_column(String(140), unique=True)
    user: Mapped[User] = relationship()
    match: Mapped[Match] = relationship()
    seat: Mapped[Seat] = relationship()


class ParkingLot(Base):
    __tablename__ = "parking"
    id: Mapped[str] = uuid_pk()
    name: Mapped[str] = mapped_column(String(120))
    total_spaces: Mapped[int] = mapped_column(Integer)
    free_spaces: Mapped[int] = mapped_column(Integer)
    accessible_spaces: Mapped[int] = mapped_column(Integer, default=0)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)


class CrowdSnapshot(Base):
    __tablename__ = "crowd"
    id: Mapped[str] = uuid_pk()
    zone: Mapped[str] = mapped_column(String(80), index=True)
    density: Mapped[float] = mapped_column(Float)
    queue_length: Mapped[int] = mapped_column(Integer)
    wait_minutes: Mapped[int] = mapped_column(Integer)
    ingress_rate: Mapped[int] = mapped_column(Integer)
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class TransportOption(Base):
    __tablename__ = "transport"
    id: Mapped[str] = uuid_pk()
    mode: Mapped[str] = mapped_column(String(40), index=True)
    route_name: Mapped[str] = mapped_column(String(120))
    eta_minutes: Mapped[int] = mapped_column(Integer)
    crowd_level: Mapped[float] = mapped_column(Float)
    carbon_grams: Mapped[int] = mapped_column(Integer)
    accessibility: Mapped[bool] = mapped_column(Boolean, default=True)


class Volunteer(Base):
    __tablename__ = "volunteers"
    id: Mapped[str] = uuid_pk()
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True)
    assigned_zone: Mapped[str] = mapped_column(String(80))
    shift_starts_at: Mapped[datetime] = mapped_column(DateTime)
    shift_ends_at: Mapped[datetime] = mapped_column(DateTime)
    latitude: Mapped[float] = mapped_column(Float, default=0)
    longitude: Mapped[float] = mapped_column(Float, default=0)
    user: Mapped[User] = relationship()


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[str] = uuid_pk()
    volunteer_id: Mapped[str] = mapped_column(ForeignKey("volunteers.id"))
    title: Mapped[str] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(40), default="open")
    priority: Mapped[str] = mapped_column(String(24), default="normal")
    due_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class FoodCourt(Base):
    __tablename__ = "food_courts"
    id: Mapped[str] = uuid_pk()
    name: Mapped[str] = mapped_column(String(120))
    zone: Mapped[str] = mapped_column(String(80))
    queue_minutes: Mapped[int] = mapped_column(Integer)
    open_stalls: Mapped[int] = mapped_column(Integer)
    vegetarian: Mapped[bool] = mapped_column(Boolean, default=True)
    halal: Mapped[bool] = mapped_column(Boolean, default=True)


class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[str] = uuid_pk()
    type: Mapped[IncidentType] = mapped_column(Enum(IncidentType))
    zone: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[str] = mapped_column(Text)
    priority: Mapped[IncidentPriority] = mapped_column(Enum(IncidentPriority), default=IncidentPriority.medium)
    status: Mapped[str] = mapped_column(String(40), default="open")
    ai_summary: Mapped[str] = mapped_column(Text, default="")
    recommended_actions: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Energy(Base):
    __tablename__ = "energy"
    id: Mapped[str] = uuid_pk()
    zone: Mapped[str] = mapped_column(String(80))
    kwh: Mapped[float] = mapped_column(Float)
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Water(Base):
    __tablename__ = "water"
    id: Mapped[str] = uuid_pk()
    zone: Mapped[str] = mapped_column(String(80))
    liters: Mapped[float] = mapped_column(Float)
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Waste(Base):
    __tablename__ = "waste"
    id: Mapped[str] = uuid_pk()
    zone: Mapped[str] = mapped_column(String(80))
    kilograms: Mapped[float] = mapped_column(Float)
    recycled_percent: Mapped[float] = mapped_column(Float)
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[str] = uuid_pk()
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    audience: Mapped[str] = mapped_column(String(40), default="all")
    title: Mapped[str] = mapped_column(String(160))
    message: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(24), default="info")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AIConversation(Base):
    __tablename__ = "ai_conversations"
    id: Mapped[str] = uuid_pk()
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    language: Mapped[str] = mapped_column(String(8), default="en")
    prompt: Mapped[str] = mapped_column(Text)
    response: Mapped[str] = mapped_column(Text)
    sources: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[str] = uuid_pk()
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(120), index=True)
    entity: Mapped[str] = mapped_column(String(80))
    entity_id: Mapped[str] = mapped_column(String(80))
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
