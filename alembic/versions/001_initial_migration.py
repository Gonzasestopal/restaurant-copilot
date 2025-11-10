"""Initial migration

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create restaurants table
    op.create_table(
        'restaurants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('timezone', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_restaurants_id'), 'restaurants', ['id'], unique=False)

    # Create menu_items table
    op.create_table(
        'menu_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('restaurant_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menu_items_id'), 'menu_items', ['id'], unique=False)

    # Create orders table
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('restaurant_id', sa.Integer(), nullable=False),
        sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('payment_type', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)

    # Create order_items table
    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('menu_item_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('total_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['menu_item_id'], ['menu_items.id'], ),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_items_id'), 'order_items', ['id'], unique=False)

    # Create daily_sales table
    op.create_table(
        'daily_sales',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('restaurant_id', sa.Integer(), nullable=False),
        sa.Column('day', sa.Date(), nullable=False),
        sa.Column('total_sales', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('avg_ticket', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('restaurant_id', 'day', name='uq_daily_sales_restaurant_day')
    )
    op.create_index(op.f('ix_daily_sales_id'), 'daily_sales', ['id'], unique=False)

    # Create metrics_dictionary table
    op.create_table(
        'metrics_dictionary',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('metric_key', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('aggregation', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('metric_key')
    )
    op.create_index(op.f('ix_metrics_dictionary_id'), 'metrics_dictionary', ['id'], unique=False)
    op.create_index(op.f('ix_metrics_dictionary_metric_key'), 'metrics_dictionary', ['metric_key'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_metrics_dictionary_metric_key'), table_name='metrics_dictionary')
    op.drop_index(op.f('ix_metrics_dictionary_id'), table_name='metrics_dictionary')
    op.drop_table('metrics_dictionary')

    op.drop_index(op.f('ix_daily_sales_id'), table_name='daily_sales')
    op.drop_table('daily_sales')

    op.drop_index(op.f('ix_order_items_id'), table_name='order_items')
    op.drop_table('order_items')

    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')

    op.drop_index(op.f('ix_menu_items_id'), table_name='menu_items')
    op.drop_table('menu_items')

    op.drop_index(op.f('ix_restaurants_id'), table_name='restaurants')
    op.drop_table('restaurants')
