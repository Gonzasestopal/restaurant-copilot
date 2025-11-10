# Database Fixtures Scripts

## seed_fixtures.py

Seeds the database with realistic restaurant data including:

- **5 Restaurants** in different Mexico City neighborhoods
- **Menu Items** for each restaurant (7-8 items per restaurant)
- **Orders** (20-50 orders per restaurant over the last 30 days)
- **Order Items** (1-5 items per order)
- **Daily Sales** aggregations for the last 30 days
- **Metrics Dictionary** entries for LLM context

### Usage

```bash
# Make sure your .env file is configured with DATABASE_URL
python -m scripts.seed_fixtures
```

**Note:** The script will automatically clear all existing fixtures before seeding new data. This ensures a clean, consistent dataset every time.

### What gets created:

- **Restaurants**: La Taquería Roma Norte, El Asador Condesa, Café del Centro, Mariscos La Playa, Pizzeria Napolitana
- **Menu Items**: Realistic Mexican restaurant menu items with categories and prices
- **Orders**: Random orders with various statuses (mostly completed), payment types, and dates over the last 30 days
- **Daily Sales**: Pre-aggregated daily sales data for analytics
- **Metrics Dictionary**: Common metrics definitions for the LLM to understand

The script automatically clears all existing fixtures before seeding to ensure a clean, consistent dataset.
