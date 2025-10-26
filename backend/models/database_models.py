"""
Database Models for BFA Audit App Calculator
============================================

SQLAlchemy ORM models for storing calculation results and benchmarks
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    JSON,
    ForeignKey,
    Index,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Project(Base):
    """Project/Audit table"""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    industry = Column(String(100), nullable=False, index=True)
    description = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    calculations = relationship("CalculationResult", back_populates="project")


class CalculationResult(Base):
    """Table for storing calculation results"""

    __tablename__ = "calculation_results"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True, index=True)
    module_name = Column(String(50), nullable=False, index=True)
    scenario_type = Column(String(50), nullable=True, index=True)
    inputs = Column(JSON, nullable=False)
    outputs = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    project = relationship("Project", back_populates="calculations")

    # Indexes
    __table_args__ = (
        Index("idx_project_module", "project_id", "module_name"),
        Index("idx_project_created", "project_id", "created_at"),
    )


class IndustryBenchmark(Base):
    """Table for industry benchmark data"""

    __tablename__ = "industry_benchmarks"

    id = Column(Integer, primary_key=True, index=True)
    industry = Column(String(100), nullable=False, index=True)
    metric_name = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(50))
    source = Column(String(200))
    date = Column(DateTime, default=datetime.utcnow, index=True)
    metadata = Column(JSON)  # Additional context

    # Unique constraint to prevent duplicate benchmarks
    __table_args__ = (
        UniqueConstraint("industry", "metric_name", "date", name="uq_benchmark"),
        Index("idx_industry_metric", "industry", "metric_name"),
    )


class MaturityAssessment(Base):
    """Table for storing maturity assessments"""

    __tablename__ = "maturity_assessments"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True, index=True)
    overall_score = Column(Float, nullable=False)
    maturity_level = Column(Integer, nullable=False)
    dimension_scores = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    project = relationship("Project")


class ScenarioAnalysis(Base):
    """Table for storing scenario analyses"""

    __tablename__ = "scenario_analyses"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True, index=True)
    scenario_type = Column(String(50), nullable=False)
    financial_metrics = Column(JSON, nullable=False)
    sensitivity_analysis = Column(JSON)
    monte_carlo_results = Column(JSON)
    recommendation = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    project = relationship("Project")


class AuditStep1Data(Base):
    """Audit Step 1: Organizational data"""

    __tablename__ = "audit_step1_data"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project")


class AuditStep2Data(Base):
    """Audit Step 2: Process data"""

    __tablename__ = "audit_step2_data"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("Project")
