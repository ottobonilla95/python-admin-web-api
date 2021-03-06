"""empty message

Revision ID: fdaa3966a25d
Revises: 21d709adeb3f
Create Date: 2020-07-21 19:11:09.445469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdaa3966a25d'
down_revision = '21d709adeb3f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=True),
    sa.Column('email', sa.String(length=40), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('profileImage', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
