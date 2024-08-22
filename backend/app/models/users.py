from sqlalchemy import Column, Integer, String, DateTime, UUID
from datetime import datetime, timezone

from ..database import Base

import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    created_date = Column(DateTime, default=datetime.now(timezone.utc))
    last_login_date = Column(DateTime, default=datetime.now(timezone.utc))