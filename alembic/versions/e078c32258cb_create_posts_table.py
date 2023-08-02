"""create posts table

Revision ID: e078c32258cb
Revises: 
Create Date: 2023-08-02 12:21:06.169029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e078c32258cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", 
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column("title", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table("posts")
