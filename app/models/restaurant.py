"""Restaurant models"""

from sqlalchemy import Column, Integer, String, DateTime, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Restaurant(Base):
    """Restaurant model"""
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    timezone = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    orders = relationship("Order", back_populates="restaurant")
    menu_items = relationship("MenuItem", back_populates="restaurant")
