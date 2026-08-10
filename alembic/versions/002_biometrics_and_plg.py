"""biometrics and plg tables

Revision ID: 002_biometrics_and_plg
Revises: 001_initial
Create Date: 2026-08-09 18:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_biometrics_and_plg'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add reverse trial and biometrics fields to users table
    op.add_column('users', sa.Column('trial_ends_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('cronotype_baseline', sa.String(length=50), nullable=True, server_default='Intermediate'))
    op.add_column('users', sa.Column('memento_mori_years_left', sa.Float(), nullable=True, server_default='45.0'))

    # Create biometric_logs table
    op.create_table(
        'biometric_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('hrv_rmssd', sa.Float(), nullable=True),
        sa.Column('hf_hrv_power', sa.Float(), nullable=True),
        sa.Column('deep_sleep_minutes', sa.Integer(), nullable=True),
        sa.Column('glucose_avg_mg_dl', sa.Float(), nullable=True),
        sa.Column('readiness_score', sa.Float(), nullable=True),
        sa.Column('allostatic_load_score', sa.Float(), nullable=True),
        sa.Column('raw_payload', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_biometric_logs_id'), 'biometric_logs', ['id'], unique=False)

    # Create dunbar_contacts table
    op.create_table(
        'dunbar_contacts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('contact_name', sa.String(length=255), nullable=False),
        sa.Column('dunbar_layer', sa.Integer(), nullable=False),
        sa.Column('oxytocin_impact_score', sa.Float(), nullable=True, server_default='50.0'),
        sa.Column('is_toxic_friction', sa.Boolean(), nullable=True, server_default='0'),
        sa.Column('last_interaction', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dunbar_contacts_id'), 'dunbar_contacts', ['id'], unique=False)

    # Create ulysses_contracts table
    op.create_table(
        'ulysses_contracts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('contract_title', sa.String(length=255), nullable=False),
        sa.Column('commitment_details', sa.Text(), nullable=False),
        sa.Column('crypto_signature', sa.String(length=64), nullable=False),
        sa.Column('penalty_financial_cents', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ulysses_contracts_id'), 'ulysses_contracts', ['id'], unique=False)

    # Create burnout_audit_logs table
    op.create_table(
        'burnout_audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lead_email', sa.String(length=255), nullable=False),
        sa.Column('burnout_risk_score', sa.Float(), nullable=False),
        sa.Column('fatigue_index', sa.Float(), nullable=False),
        sa.Column('recommended_module', sa.String(length=50), nullable=False),
        sa.Column('audit_report_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_burnout_audit_logs_id'), 'burnout_audit_logs', ['id'], unique=False)
    op.create_index(op.f('ix_burnout_audit_logs_lead_email'), 'burnout_audit_logs', ['lead_email'], unique=False)


def downgrade() -> None:
    op.drop_table('burnout_audit_logs')
    op.drop_table('ulysses_contracts')
    op.drop_table('dunbar_contacts')
    op.drop_table('biometric_logs')
    op.drop_column('users', 'memento_mori_years_left')
    op.drop_column('users', 'cronotype_baseline')
    op.drop_column('users', 'trial_ends_at')
