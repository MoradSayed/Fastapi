"""add content column to posts table

Revision ID: 293b92bd788e
Revises: e078c32258cb
Create Date: 2023-08-02 12:58:03.800144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '293b92bd788e'
down_revision = 'e078c32258cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
