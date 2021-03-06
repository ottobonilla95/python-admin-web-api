"""empty message

Revision ID: 31d51c5d12bc
Revises: 30dcf32a6897
Create Date: 2020-07-30 15:17:09.169733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31d51c5d12bc'
down_revision = '30dcf32a6897'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profile_image', sa.String(length=100), nullable=True))
    op.drop_column('user', 'profileImage')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('profileImage', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('user', 'profile_image')
    # ### end Alembic commands ###
