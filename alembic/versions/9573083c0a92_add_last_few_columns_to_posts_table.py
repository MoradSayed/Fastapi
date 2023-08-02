"""add last few columns to posts table

Revision ID: 9573083c0a92
Revises: 6a3d18b9ba0c
Create Date: 2023-08-02 13:34:46.994467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9573083c0a92'
down_revision = '6a3d18b9ba0c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),)


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
