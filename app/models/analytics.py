"""Analytics models"""

from sqlalchemy import Column, Integer, Date, Numeric, DateTime, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class DailySales(Base):
    """Daily sales aggregation model"""
    __tablename__ = "daily_sales"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    day = Column(Date, nullable=False)
    total_sales = Column(Numeric(10, 2), nullable=False)
    avg_ticket = Column(Numeric(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    restaurant = relationship("Restaurant")

    # Unique constraint on restaurant_id and day
    __table_args__ = (
        UniqueConstraint("restaurant_id", "day", name="uq_daily_sales_restaurant_day"),
    )


class MetricsDictionary(Base):
    """Metrics dictionary for LLM context"""
    __tablename__ = "metrics_dictionary"

    id = Column(Integer, primary_key=True, index=True)
    metric_key = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False)
    aggregation = Column(String)  # e.g., "SUM", "AVG", "COUNT"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
