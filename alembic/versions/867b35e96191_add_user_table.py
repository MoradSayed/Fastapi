"""add user table

Revision ID: 867b35e96191
Revises: 293b92bd788e
Create Date: 2023-08-02 13:13:55.654200

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '867b35e96191'
down_revision = '293b92bd788e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable=False), 
                    sa.Column("email", sa.String(), nullable=False), 
                    sa.Column("password", sa.String(), nullable=False), 
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default = sa.text("now()"), nullable=False), 
                    sa.PrimaryKeyConstraint("id"), 
                    sa.UniqueConstraint("email"))


def downgrade() -> None:
    op.drop_table("users")
    pass
