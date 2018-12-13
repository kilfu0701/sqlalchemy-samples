from sqlalchemy import Integer, VARCHAR, TIMESTAMP, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

Base = declarative_base()

from .role import Role

class Permission(Base):
    __tablename__ = 'permissions'

    id           = Column(Integer, primary_key=True)
    roles        = Column(Integer, ForeignKey(Role.__table__.columns.id), nullable=False)
    allow        = Column(VARCHAR(length=100), nullable=False)
    display_name = Column(VARCHAR(length=100), nullable=False)
    created_at   = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at   = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
