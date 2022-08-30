"""add user table

Revision ID: c43c9d87cd6a
Revises: 000b514ea4b7
Create Date: 2022-08-29 22:52:12.556260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c43c9d87cd6a'
down_revision = '000b514ea4b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
