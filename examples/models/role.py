from sqlalchemy import Integer, VARCHAR, TIMESTAMP, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Role(Base):
    __tablename__ = 'roles'

    id           = Column(Integer, primary_key=True)
    display_name = Column(VARCHAR(length=14), nullable=False)
    created_at   = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at   = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
