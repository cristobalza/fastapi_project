"""add a few more columns to posts table

Revision ID: e2fd2d6d2eb6
Revises: f35319c7b3a8
Create Date: 2022-08-30 19:41:25.539788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2fd2d6d2eb6'
down_revision = 'f35319c7b3a8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published',
                                     sa.Boolean(), 
                                     nullable=False, 
                                     server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at',
                                     sa.TIMESTAMP(timezone=True),
                                     nullable=False, 
                                     server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
