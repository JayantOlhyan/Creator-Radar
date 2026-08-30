"""Phase 1 Creator Watchlist Schema Migration

Revision ID: 002_phase1_creator_watchlist
Revises: 001_initial_schema
Create Date: 2026-08-30 15:45:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_phase1_creator_watchlist'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add status and check lifecycle columns to creators
    op.add_column('creators', sa.Column('status', sa.String(length=50), nullable=False, server_default='ACTIVE'))
    op.add_column('creators', sa.Column('last_checked_at', sa.DateTime(), nullable=True))
    op.add_column('creators', sa.Column('last_successful_check_at', sa.DateTime(), nullable=True))
    op.add_column('creators', sa.Column('last_error_at', sa.DateTime(), nullable=True))
    op.add_column('creators', sa.Column('last_error_message', sa.Text(), nullable=True))
    op.add_column('creators', sa.Column('check_interval_minutes', sa.Integer(), nullable=False, server_default='60'))
    op.create_index(op.f('ix_creators_status'), 'creators', ['status'], unique=False)

    # Add media dimension & duration fields to post_media
    op.add_column('post_media', sa.Column('mime_type', sa.String(length=100), nullable=True))
    op.add_column('post_media', sa.Column('duration', sa.Integer(), nullable=True))
    op.add_column('post_media', sa.Column('width', sa.Integer(), nullable=True))
    op.add_column('post_media', sa.Column('height', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('post_media', 'height')
    op.drop_column('post_media', 'width')
    op.drop_column('post_media', 'duration')
    op.drop_column('post_media', 'mime_type')

    op.drop_index(op.f('ix_creators_status'), table_name='creators')
    op.drop_column('creators', 'check_interval_minutes')
    op.drop_column('creators', 'last_error_message')
    op.drop_column('creators', 'last_error_at')
    op.drop_column('creators', 'last_successful_check_at')
    op.drop_column('creators', 'last_checked_at')
    op.drop_column('creators', 'status')
