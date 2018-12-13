from sqlalchemy import Integer, VARCHAR, TIMESTAMP, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

from .role import Role
from .image import Image

class User(Base):
    __tablename__ = 'users'

    id           = Column(Integer, primary_key=True)
    email        = Column(VARCHAR(length=256), nullable=False)
    password     = Column(VARCHAR(length=2000), nullable=False)
    role_id      = Column(Integer, ForeignKey('roles.id'), nullable=False)
    image_id     = Column(Integer, ForeignKey('images.id'), nullable=False, default=1)
    first_name   = Column(VARCHAR(length=100), nullable=False)
    last_name    = Column(VARCHAR(length=100), nullable=False)
    created_at   = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at   = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
