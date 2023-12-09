from sqlalchemy import Column, Integer, String

from src.db.base import Base


class UrlModel(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    gcs_url = Column(String, index=True)
