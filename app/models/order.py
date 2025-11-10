"""Order models"""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum, TypeDecorator
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class EnumValue(TypeDecorator):
    """TypeDecorator that stores enum values (lowercase strings) instead of member names"""
    impl = String
    cache_ok = True

    def __init__(self, enum_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_class = enum_class

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, self.enum_class):
            return value.value
        if isinstance(value, str):
            # If it's already a string, validate it's a valid enum value
            valid_values = [e.value for e in self.enum_class]
            if value in valid_values:
                return value
            # Try to find by value
            for e in self.enum_class:
                if e.value == value:
                    return e.value
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        # Convert string value back to enum member
        for e in self.enum_class:
            if e.value == value:
                return e
        return value


class OrderStatus(str, enum.Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentType(str, enum.Enum):
    """Payment type enumeration"""
    CASH = "cash"
    CARD = "card"
    DIGITAL = "digital"


class Order(Base):
    """Order model"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    payment_type = Column(EnumValue(PaymentType, length=20), nullable=False)
    status = Column(EnumValue(OrderStatus, length=20), default=OrderStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    restaurant = relationship("Restaurant", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """Order item model"""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")
