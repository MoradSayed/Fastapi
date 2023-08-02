"""add foreign-key to posts table

Revision ID: 6a3d18b9ba0c
Revises: 867b35e96191
Create Date: 2023-08-02 13:25:35.172018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a3d18b9ba0c'
down_revision = '867b35e96191'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", 
                          source_table="posts", 
                          referent_table="users", 
                          local_cols=["owner_id"], 
                          remote_cols=["id"], 
                          ondelete="CASCADE")

def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
