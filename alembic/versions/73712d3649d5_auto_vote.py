"""auto-vote

Revision ID: 73712d3649d5
Revises: 9573083c0a92
Create Date: 2023-08-02 13:42:44.858063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73712d3649d5'
down_revision = '9573083c0a92'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_table('votes')
    # ### end Alembic commands ###
