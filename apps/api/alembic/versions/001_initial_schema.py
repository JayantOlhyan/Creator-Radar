"""Initial Schema Migration for CreatorRadar

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-08-30 15:15:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # User Profiles
    op.create_table(
        'user_profiles',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('niche', sa.String(length=255), nullable=True),
        sa.Column('content_goals', sa.JSON(), nullable=False),
        sa.Column('tone_of_voice', sa.String(length=255), nullable=True),
        sa.Column('target_audience', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )

    # Creators
    op.create_table(
        'creators',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('profile_url', sa.String(length=512), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_creators_username'), 'creators', ['username'], unique=False)
    op.create_index(op.f('ix_creators_platform'), 'creators', ['platform'], unique=False)

    # Creator Sources
    op.create_table(
        'creator_sources',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('creator_id', sa.String(), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('source_identifier', sa.String(length=255), nullable=False),
        sa.Column('config', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['creators.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Posts (with deduplication unique constraint)
    op.create_table(
        'posts',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('creator_id', sa.String(), nullable=False),
        sa.Column('external_id', sa.String(length=255), nullable=False),
        sa.Column('url', sa.String(length=1024), nullable=False),
        sa.Column('content_type', sa.String(length=50), nullable=False),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('detected_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['creators.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('creator_id', 'external_id', name='uq_creator_external_post')
    )
    op.create_index(op.f('ix_posts_creator_id'), 'posts', ['creator_id'], unique=False)
    op.create_index(op.f('ix_posts_external_id'), 'posts', ['external_id'], unique=False)
    op.create_index(op.f('ix_posts_status'), 'posts', ['status'], unique=False)

    # Post Media
    op.create_table(
        'post_media',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('post_id', sa.String(), nullable=False),
        sa.Column('media_type', sa.String(length=50), nullable=False),
        sa.Column('media_url', sa.String(length=1024), nullable=False),
        sa.Column('thumbnail_url', sa.String(length=1024), nullable=True),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_media_post_id'), 'post_media', ['post_id'], unique=False)

    # Post Analysis
    op.create_table(
        'post_analysis',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('post_id', sa.String(), nullable=False),
        sa.Column('topic', sa.String(length=255), nullable=False),
        sa.Column('hook', sa.Text(), nullable=False),
        sa.Column('hook_type', sa.String(length=100), nullable=False),
        sa.Column('format', sa.String(length=100), nullable=False),
        sa.Column('narrative_structure', sa.Text(), nullable=False),
        sa.Column('target_audience', sa.String(length=255), nullable=False),
        sa.Column('emotional_trigger', sa.String(length=100), nullable=False),
        sa.Column('cta', sa.Text(), nullable=False),
        sa.Column('visual_structure', sa.Text(), nullable=False),
        sa.Column('editing_style', sa.String(length=255), nullable=False),
        sa.Column('content_mechanism', sa.Text(), nullable=False),
        sa.Column('why_it_works', sa.Text(), nullable=False),
        sa.Column('relevance_score', sa.Float(), nullable=False),
        sa.Column('originality_score', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('post_id')
    )

    # Content Patterns
    op.create_table(
        'content_patterns',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('structure', sa.Text(), nullable=False),
        sa.Column('example_count', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Knowledge Items
    op.create_table(
        'knowledge_items',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('item_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tags', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_items_user_id'), 'knowledge_items', ['user_id'], unique=False)

    # Content Opportunities
    op.create_table(
        'content_opportunities',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('post_analysis_id', sa.String(), nullable=True),
        sa.Column('pattern_id', sa.String(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('hook', sa.Text(), nullable=False),
        sa.Column('concept', sa.Text(), nullable=False),
        sa.Column('format', sa.String(length=100), nullable=False),
        sa.Column('reasoning', sa.Text(), nullable=False),
        sa.Column('relevance_score', sa.Float(), nullable=False),
        sa.Column('originality_score', sa.Float(), nullable=False),
        sa.Column('effort_score', sa.Float(), nullable=False),
        sa.Column('priority_score', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['post_analysis_id'], ['post_analysis.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['pattern_id'], ['content_patterns.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_opportunities_user_id'), 'content_opportunities', ['user_id'], unique=False)
    op.create_index(op.f('ix_content_opportunities_status'), 'content_opportunities', ['status'], unique=False)

    # Notifications
    op.create_table(
        'notifications',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('opportunity_id', sa.String(), nullable=True),
        sa.Column('channel', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('sent_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['opportunity_id'], ['content_opportunities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_table('notifications')
    op.drop_table('content_opportunities')
    op.drop_table('knowledge_items')
    op.drop_table('content_patterns')
    op.drop_table('post_analysis')
    op.drop_table('post_media')
    op.drop_table('posts')
    op.drop_table('creator_sources')
    op.drop_table('creators')
    op.drop_table('user_profiles')
    op.drop_table('users')
