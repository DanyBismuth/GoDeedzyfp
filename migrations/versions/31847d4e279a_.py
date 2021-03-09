"""empty message

Revision ID: 31847d4e279a
Revises: e394a159ede1
Create Date: 2021-03-02 18:34:39.363764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31847d4e279a'
down_revision = 'e394a159ede1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=512), nullable=False),
    sa.Column('date', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'challenges', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'challenges', type_='unique')
    op.drop_table('notifications')
    # ### end Alembic commands ###
