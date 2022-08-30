"""add content column to posts table

Revision ID: 000b514ea4b7
Revises: ad26465c0e28
Create Date: 2022-08-29 22:43:47.276931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '000b514ea4b7'
down_revision = 'ad26465c0e28'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
