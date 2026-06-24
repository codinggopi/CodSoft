from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    password = Column(String, nullable=True)
    role = Column(String)
    security_question = Column(String, nullable=True)
    security_answer = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    company = relationship("Company", back_populates="employer", uselist=False)
    jobs = relationship("Job", back_populates="employer", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="candidate", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    profile_views_as_employer = relationship("ProfileView", foreign_keys="[ProfileView.employer_id]", cascade="all, delete-orphan")
    profile_views_as_candidate = relationship("ProfileView", foreign_keys="[ProfileView.candidate_id]", cascade="all, delete-orphan")


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    employer_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    logo_url = Column(String)
    industry = Column(String)
    size = Column(String)
    location = Column(String)
    founded_year = Column(String)
    website = Column(String)
    linkedin = Column(String)
    mission = Column(Text)
    vision = Column(Text)
    benefits = Column(Text)
    description = Column(Text)
    status = Column(String, default="Active") # 'Active', 'Disabled', 'Pending'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    employer = relationship("User", back_populates="company")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String)
    salary = Column(String)
    job_type = Column(String) # 'Full Time', 'Part Time', 'Internship', 'Remote'
    description = Column(Text)
    requirements = Column(Text)
    skills = Column(Text)
    deadline = Column(String)
    status = Column(String, default="Active") # 'Active', 'Closed'
    employer_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    employer = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    candidate_id = Column(Integer, ForeignKey("users.id"))
    resume_url = Column(String)
    cover_letter = Column(Text)
    status = Column(String, default="Pending") # 'Pending', 'Reviewed', 'Shortlisted', 'Interview', 'Hired', 'Rejected'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    job = relationship("Job", back_populates="applications")
    candidate = relationship("User", back_populates="applications")
    interviews = relationship("Interview", back_populates="application", cascade="all, delete-orphan")


class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    scheduled_time = Column(DateTime)
    meeting_link = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    application = relationship("Application", back_populates="interviews")


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="notifications")


class ProfileView(Base):
    __tablename__ = "profile_views"
    id = Column(Integer, primary_key=True, index=True)
    employer_id = Column(Integer, ForeignKey("users.id"))
    candidate_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # We do not strictly need back_populates here since we only cascade delete from User
