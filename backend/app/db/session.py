from collections.abc import Generator
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from app.core.config import get_settings


class Base(DeclarativeBase):
    """Base class for STADIUMAI SQLAlchemy models."""


settings = get_settings()
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database() -> None:
    from app.models.domain import CrowdSnapshot, Energy, FoodCourt, Gate, Match, ParkingLot, Role, RoleName, TransportOption, Waste, Water

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        for role, description in [
            (RoleName.fan, "Tournament visitor"),
            (RoleName.volunteer, "Venue volunteer"),
            (RoleName.organizer, "Operations organizer"),
            (RoleName.admin, "System administrator"),
        ]:
            if not db.scalar(select(Role).where(Role.name == role)):
                db.add(Role(name=role, description=description))
        if not db.scalar(select(Gate)):
            db.add_all([
                Gate(code="A", name="North Gate", latitude=25.960, longitude=-80.239, accessibility=True, current_wait_minutes=8, congestion_score=0.34),
                Gate(code="B", name="Metro Gate", latitude=25.961, longitude=-80.236, accessibility=True, current_wait_minutes=28, congestion_score=0.88),
                Gate(code="C", name="West Gate", latitude=25.956, longitude=-80.243, accessibility=False, current_wait_minutes=16, congestion_score=0.62),
                Gate(code="D", name="East Gate", latitude=25.955, longitude=-80.241, accessibility=True, current_wait_minutes=6, congestion_score=0.28),
            ])
            db.add_all([
                Match(home_team="USA", away_team="Canada", venue="Miami Stadium", starts_at=datetime.utcnow() + timedelta(days=7), status="scheduled"),
                ParkingLot(name="Lot C", total_spaces=1800, free_spaces=728, accessible_spaces=46, latitude=25.965, longitude=-80.235),
                CrowdSnapshot(zone="Gate B", density=0.88, queue_length=620, wait_minutes=28, ingress_rate=900),
                CrowdSnapshot(zone="Gate D", density=0.28, queue_length=90, wait_minutes=6, ingress_rate=420),
                TransportOption(mode="metro", route_name="Line 2 Stadium Express", eta_minutes=4, crowd_level=0.72, carbon_grams=40, accessibility=True),
                TransportOption(mode="bus", route_name="Route 26 Shuttle", eta_minutes=11, crowd_level=0.45, carbon_grams=180, accessibility=True),
                FoodCourt(name="North Market", zone="North Stand", queue_minutes=7, open_stalls=14, vegetarian=True, halal=True),
                Energy(zone="North Stand", kwh=9200),
                Water(zone="Restrooms North", liters=32000),
                Waste(zone="North Stand", kilograms=1800, recycled_percent=62),
            ])
        db.commit()
