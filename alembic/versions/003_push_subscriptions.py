"""push subscriptions table

Revision ID: 003_push_subscriptions
Revises: 002_biometrics_and_plg
Create Date: 2026-08-09 18:40:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '003_push_subscriptions'
down_revision: Union[str, None] = '002_biometrics_and_plg'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'push_subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('endpoint', sa.Text(), nullable=False),
        sa.Column('p256dh', sa.String(length=255), nullable=False),
        sa.Column('auth', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('endpoint')
    )
    op.create_index(op.f('ix_push_subscriptions_endpoint'), 'push_subscriptions', ['endpoint'], unique=True)
    op.create_index(op.f('ix_push_subscriptions_id'), 'push_subscriptions', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_push_subscriptions_id'), table_name='push_subscriptions')
    op.drop_index(op.f('ix_push_subscriptions_endpoint'), table_name='push_subscriptions')
    op.drop_table('push_subscriptions')
