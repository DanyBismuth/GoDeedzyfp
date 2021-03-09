"""empty message

Revision ID: 2855bfaa1d99
Revises: 7c4e60f5afd1
Create Date: 2021-03-04 18:55:15.559404

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2855bfaa1d99'
down_revision = '7c4e60f5afd1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('description')
    op.drop_table('users_challenges')
    op.drop_table('achieved')
    op.drop_table('challenges')
    op.add_column('user', sa.Column('achieved_challenge', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'achieved_challenge')
    op.create_table('challenges',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('challenges_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('title', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('achieved_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('challenge', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='challenges_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='challenges_pkey'),
    sa.UniqueConstraint('id', name='challenges_id_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('achieved',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('challenge_achieved', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='achieved_pkey')
    )
    op.create_table('users_challenges',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('challenge_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['challenge_id'], ['challenges.id'], name='users_challenges_challenge_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='users_challenges_user_id_fkey'),
    sa.PrimaryKeyConstraint('user_id', 'challenge_id', name='users_challenges_pkey')
    )
    op.create_table('description',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=512), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=2000), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='description_pkey')
    )
    # ### end Alembic commands ###
