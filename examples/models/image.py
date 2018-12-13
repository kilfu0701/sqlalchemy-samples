from enum import IntEnum

from sqlalchemy import Integer, VARCHAR, BOOLEAN, TIMESTAMP, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

Base = declarative_base()

class ImageUseType(IntEnum):
    UseTypeGeneral  = 1
    UseTypeUserIcon = 2

class ImageStatus(IntEnum):
    StatusUploaded   = 1
    StatusConverting = 2
    StatusOK         = 3

class Image(Base):
    __tablename__ = 'images'

    id          = Column(Integer, primary_key=True)
    use_type    = Column(Integer, nullable=False)
    alt         = Column(VARCHAR(length=120), nullable=False, default='')
    caption     = Column(VARCHAR(length=255), nullable=False, default='')
    filename    = Column(VARCHAR(length=300), nullable=False)
    width       = Column(Integer)
    height      = Column(Integer)
    filesize    = Column(Integer)
    digest      = Column(VARCHAR(length=32))
    status      = Column(Integer, nullable=False, default=1)
    deleted_flg = Column(BOOLEAN, nullable=False, default=False)
    created_at  = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at  = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    @validates('use_type')
    def validate_use_type(self, key, use_type):
        use_type_ints = list(map(int, ImageUseType))
        if use_type not in use_type_ints:
            raise ValueError('Unsupported use_type.')

        return use_type
