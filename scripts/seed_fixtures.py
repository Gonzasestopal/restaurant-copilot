"""Seed database with realistic fixtures"""

import random
from datetime import datetime, timedelta, date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.restaurant import Restaurant
from app.models.menu import MenuItem
from app.models.order import Order, OrderItem, OrderStatus, PaymentType
from app.models.analytics import DailySales, MetricsDictionary


# Restaurant data
RESTAURANTS = [
    {"name": "La Taquería Roma Norte", "location": "Roma Norte, CDMX", "timezone": "America/Mexico_City"},
    {"name": "El Asador Condesa", "location": "Condesa, CDMX", "timezone": "America/Mexico_City"},
    {"name": "Café del Centro", "location": "Centro Histórico, CDMX", "timezone": "America/Mexico_City"},
    {"name": "Mariscos La Playa", "location": "Polanco, CDMX", "timezone": "America/Mexico_City"},
    {"name": "Pizzeria Napolitana", "location": "Coyoacán, CDMX", "timezone": "America/Mexico_City"},
]

# Menu items by category
MENU_ITEMS = {
    "La Taquería Roma Norte": [
        {"name": "Tacos al Pastor", "category": "Tacos", "price": 25.00},
        {"name": "Tacos de Asada", "category": "Tacos", "price": 28.00},
        {"name": "Tacos de Pollo", "category": "Tacos", "price": 24.00},
        {"name": "Quesadilla", "category": "Antojitos", "price": 35.00},
        {"name": "Torta Ahogada", "category": "Tortas", "price": 45.00},
        {"name": "Agua de Horchata", "category": "Bebidas", "price": 15.00},
        {"name": "Coca Cola", "category": "Bebidas", "price": 20.00},
        {"name": "Cerveza Corona", "category": "Bebidas", "price": 35.00},
    ],
    "El Asador Condesa": [
        {"name": "Arrachera", "category": "Carnes", "price": 180.00},
        {"name": "Ribeye", "category": "Carnes", "price": 220.00},
        {"name": "Pollo Asado", "category": "Carnes", "price": 150.00},
        {"name": "Ensalada César", "category": "Ensaladas", "price": 85.00},
        {"name": "Papas Fritas", "category": "Acompañamientos", "price": 45.00},
        {"name": "Vino Tinto", "category": "Bebidas", "price": 120.00},
        {"name": "Agua Mineral", "category": "Bebidas", "price": 25.00},
    ],
    "Café del Centro": [
        {"name": "Café Americano", "category": "Café", "price": 35.00},
        {"name": "Cappuccino", "category": "Café", "price": 45.00},
        {"name": "Latte", "category": "Café", "price": 50.00},
        {"name": "Croissant", "category": "Panadería", "price": 30.00},
        {"name": "Pastel de Chocolate", "category": "Postres", "price": 55.00},
        {"name": "Sandwich Club", "category": "Sandwiches", "price": 75.00},
        {"name": "Jugo de Naranja", "category": "Bebidas", "price": 40.00},
    ],
    "Mariscos La Playa": [
        {"name": "Ceviche de Pescado", "category": "Ceviches", "price": 120.00},
        {"name": "Camarones al Ajillo", "category": "Platos Fuertes", "price": 180.00},
        {"name": "Pescado a la Talla", "category": "Platos Fuertes", "price": 200.00},
        {"name": "Cóctel de Camarón", "category": "Cócteles", "price": 95.00},
        {"name": "Aguachile", "category": "Ceviches", "price": 110.00},
        {"name": "Cerveza Pacífico", "category": "Bebidas", "price": 40.00},
        {"name": "Agua de Jamaica", "category": "Bebidas", "price": 20.00},
    ],
    "Pizzeria Napolitana": [
        {"name": "Pizza Margherita", "category": "Pizzas", "price": 150.00},
        {"name": "Pizza Pepperoni", "category": "Pizzas", "price": 170.00},
        {"name": "Pizza Hawaiana", "category": "Pizzas", "price": 175.00},
        {"name": "Pizza Cuatro Quesos", "category": "Pizzas", "price": 180.00},
        {"name": "Aros de Cebolla", "category": "Aperitivos", "price": 65.00},
        {"name": "Refresco", "category": "Bebidas", "price": 25.00},
        {"name": "Cerveza", "category": "Bebidas", "price": 45.00},
    ],
}

# Metrics dictionary
METRICS = [
    {
        "metric_key": "total_sales",
        "description": "Total revenue from all orders",
        "aggregation": "SUM"
    },
    {
        "metric_key": "avg_ticket",
        "description": "Average order value",
        "aggregation": "AVG"
    },
    {
        "metric_key": "order_count",
        "description": "Total number of orders",
        "aggregation": "COUNT"
    },
    {
        "metric_key": "items_sold",
        "description": "Total quantity of items sold",
        "aggregation": "SUM"
    },
    {
        "metric_key": "daily_revenue",
        "description": "Revenue per day",
        "aggregation": "SUM"
    },
    {
        "metric_key": "top_selling_item",
        "description": "Most frequently ordered menu item",
        "aggregation": "COUNT"
    },
]


def seed_restaurants(db: Session):
    """Seed restaurants"""
    print("Seeding restaurants...")
    restaurants = []
    for rest_data in RESTAURANTS:
        restaurant = Restaurant(
            name=rest_data["name"],
            location=rest_data["location"],
            timezone=rest_data["timezone"]
        )
        db.add(restaurant)
        restaurants.append(restaurant)
    db.commit()
    print(f"✓ Created {len(restaurants)} restaurants")
    return restaurants


def seed_menu_items(db: Session, restaurants: list[Restaurant]):
    """Seed menu items for each restaurant"""
    print("Seeding menu items...")
    menu_items_map = {}

    for restaurant in restaurants:
        items = MENU_ITEMS.get(restaurant.name, [])
        restaurant_items = []
        for item_data in items:
            menu_item = MenuItem(
                restaurant_id=restaurant.id,
                name=item_data["name"],
                category=item_data["category"],
                price=Decimal(str(item_data["price"]))
            )
            db.add(menu_item)
            restaurant_items.append(menu_item)
        menu_items_map[restaurant.id] = restaurant_items
        db.commit()
        print(f"✓ Created {len(restaurant_items)} menu items for {restaurant.name}")

    return menu_items_map


def seed_orders(db: Session, restaurants: list[Restaurant], menu_items_map: dict):
    """Seed orders with realistic data"""
    print("Seeding orders...")

    # Generate orders for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    order_statuses = list(OrderStatus)
    payment_types = list(PaymentType)

    total_orders = 0

    for restaurant in restaurants:
        restaurant_items = menu_items_map[restaurant.id]
        if not restaurant_items:
            continue

        # Generate 20-50 orders per restaurant
        num_orders = random.randint(20, 50)

        for _ in range(num_orders):
            # Random date within last 30 days
            order_date = start_date + timedelta(
                seconds=random.randint(0, int((end_date - start_date).total_seconds()))
            )

            # Random status (most should be completed)
            status = random.choices(
                order_statuses,
                weights=[0.05, 0.05, 0.05, 0.05, 0.75, 0.05]  # 75% completed
            )[0]

            # Random payment type
            payment_type = random.choice(payment_types)

            # Create order items (1-5 items per order)
            num_items = random.randint(1, 5)
            selected_items = random.choices(restaurant_items, k=num_items)

            order_items = []
            order_total = Decimal('0.00')

            for menu_item in selected_items:
                quantity = random.randint(1, 3)
                item_total = menu_item.price * quantity
                order_total += item_total

                order_item = OrderItem(
                    menu_item_id=menu_item.id,
                    quantity=quantity,
                    total_price=item_total
                )
                order_items.append(order_item)

            # Create order (TypeDecorator will handle enum value conversion)
            order = Order(
                restaurant_id=restaurant.id,
                total=order_total,
                payment_type=payment_type,
                status=status,
                created_at=order_date
            )
            db.add(order)
            db.flush()  # Get order.id

            # Associate order items with order
            for order_item in order_items:
                order_item.order_id = order.id
                db.add(order_item)

            total_orders += 1

    db.commit()
    print(f"✓ Created {total_orders} orders")
    return total_orders


def seed_daily_sales(db: Session, restaurants: list[Restaurant]):
    """Seed daily sales aggregations"""
    print("Seeding daily sales...")

    # Generate daily sales for the last 30 days
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    total_daily_sales = 0

    for restaurant in restaurants:
        current_date = start_date
        while current_date <= end_date:
            # Get orders for this restaurant on this date
            orders = db.query(Order).filter(
                Order.restaurant_id == restaurant.id,
                Order.created_at >= datetime.combine(current_date, datetime.min.time()),
                Order.created_at < datetime.combine(current_date + timedelta(days=1), datetime.min.time()),
                Order.status == OrderStatus.COMPLETED
            ).all()

            if orders:
                total_sales = sum(order.total for order in orders)
                avg_ticket = total_sales / len(orders) if orders else Decimal('0.00')

                daily_sale = DailySales(
                    restaurant_id=restaurant.id,
                    day=current_date,
                    total_sales=total_sales,
                    avg_ticket=avg_ticket
                )
                db.add(daily_sale)
                total_daily_sales += 1

            current_date += timedelta(days=1)

    db.commit()
    print(f"✓ Created {total_daily_sales} daily sales records")
    return total_daily_sales


def seed_metrics_dictionary(db: Session):
    """Seed metrics dictionary"""
    print("Seeding metrics dictionary...")

    for metric_data in METRICS:
        metric = MetricsDictionary(
            metric_key=metric_data["metric_key"],
            description=metric_data["description"],
            aggregation=metric_data["aggregation"]
        )
        db.add(metric)

    db.commit()
    print(f"✓ Created {len(METRICS)} metrics dictionary entries")


def clear_all_fixtures(db: Session):
    """Clear all existing fixtures from the database"""
    print("Clearing existing fixtures...")

    # Delete in order to respect foreign key constraints
    db.query(OrderItem).delete()
    db.query(Order).delete()
    db.query(MenuItem).delete()
    db.query(DailySales).delete()
    db.query(Restaurant).delete()
    db.query(MetricsDictionary).delete()
    db.commit()

    print("✓ Cleared all existing fixtures")


def main():
    """Main seeding function"""
    print("=" * 50)
    print("Starting database seeding...")
    print("=" * 50)

    db = SessionLocal()

    try:
        # Always clear old fixtures first
        clear_all_fixtures(db)

        # Seed in order
        restaurants = seed_restaurants(db)
        menu_items_map = seed_menu_items(db, restaurants)
        seed_orders(db, restaurants, menu_items_map)
        seed_daily_sales(db, restaurants)
        seed_metrics_dictionary(db)

        print("=" * 50)
        print("✓ Database seeding completed successfully!")
        print("=" * 50)

    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
