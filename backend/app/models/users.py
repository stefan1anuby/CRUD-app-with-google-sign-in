from sqlalchemy import Column, Integer, String, DateTime, UUID, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

from ..database import Base

import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    created_date = Column(DateTime, default=datetime.now(timezone.utc))
    last_login_date = Column(DateTime, default=datetime.now(timezone.utc))

    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")

class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    content = Column(String(100), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    user = relationship("User", back_populates="notes")