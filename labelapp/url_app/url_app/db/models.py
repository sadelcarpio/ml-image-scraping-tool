import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UUID, Boolean, Table
from sqlalchemy.orm import relationship

from url_app.db.base import Base


class UrlModel(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    gcs_url = Column(String, unique=True, nullable=False)
    hashed_url = Column(String(64), nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, index=True, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    labeled = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete="SET NULL"), nullable=True)


UserProjectModel = Table(
    "users_projects",
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True)
)


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    projects = relationship('ProjectModel', secondary=UserProjectModel, back_populates='users')


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False, unique=True)
    users = relationship('UserModel', secondary=UserProjectModel, back_populates='projects')
