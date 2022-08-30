"""create posts table

Revision ID: ad26465c0e28
Revises: 
Create Date: 2022-08-29 22:31:37.976497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad26465c0e28'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
    pass
