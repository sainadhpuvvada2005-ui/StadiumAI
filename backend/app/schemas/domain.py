from datetime import datetime
from typing import Any
from pydantic import BaseModel, EmailStr, Field
from app.models.domain import IncidentPriority, IncidentType, RoleName


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: RoleName


class RegisterIn(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=160)
    password: str = Field(min_length=10, max_length=128)
    role: RoleName = RoleName.fan
    preferred_language: str = Field(default="en", pattern="^(en|es|fr|pt|ar|hi)$")


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordIn(BaseModel):
    email: EmailStr


class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: RoleName
    preferred_language: str
    model_config = {"from_attributes": True}


class AIChatIn(BaseModel):
    message: str = Field(min_length=2, max_length=1200)
    language: str = Field(default="en", pattern="^(en|es|fr|pt|ar|hi)$")
    context: dict[str, Any] = Field(default_factory=dict)


class AIChatOut(BaseModel):
    answer: str
    language: str
    sources: list[str]
    recommendations: list[str] = []


class IncidentCreate(BaseModel):
    type: IncidentType
    zone: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=5, max_length=2000)


class IncidentOut(BaseModel):
    id: str
    type: IncidentType
    zone: str
    description: str
    priority: IncidentPriority
    status: str
    ai_summary: str
    recommended_actions: dict[str, Any]
    created_at: datetime


class DashboardMetric(BaseModel):
    label: str
    value: str | int | float
    trend: float = 0


class CrowdInsight(BaseModel):
    zone: str
    density: float
    queue_length: int
    wait_minutes: int
    risk: str
    ai_summary: str
    alternative_route: str


class SustainabilityOut(BaseModel):
    water_liters: float
    electricity_kwh: float
    waste_kg: float
    carbon_kg: float
    recommendations: list[str]
