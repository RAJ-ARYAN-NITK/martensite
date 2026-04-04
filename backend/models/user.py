from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from db import Base
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

# ── SQLAlchemy ORM ───────────────────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"
    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email      = Column(String, unique=True, nullable=False, index=True)
    name       = Column(String, nullable=False)
    password   = Column(String, nullable=False)   # bcrypt hashed
    role       = Column(String, default="customer")  # customer | admin | driver
    is_active  = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# ── Pydantic Schemas ─────────────────────────────────────────────────────────
class UserRegister(BaseModel):
    email: str
    name: str
    password: str
    role: Optional[str] = "customer"

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse