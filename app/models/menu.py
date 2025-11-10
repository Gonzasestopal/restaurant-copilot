"""Menu models"""

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class MenuItem(Base):
    """Menu item model"""
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    restaurant = relationship("Restaurant", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item")
