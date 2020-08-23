"""empty message

Revision ID: 30dcf32a6897
Revises: 49bb46f1faf8
Create Date: 2020-07-30 15:06:01.190716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30dcf32a6897'
down_revision = '49bb46f1faf8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agent', sa.Column('creation_date', sa.DateTime(), nullable=True))
    op.add_column('company', sa.Column('creation_date', sa.DateTime(), nullable=True))
    op.add_column('customer', sa.Column('creation_date', sa.DateTime(), nullable=True))
    op.add_column('planogram', sa.Column('creation_date', sa.DateTime(), nullable=True))
    op.add_column('product', sa.Column('creation_date', sa.DateTime(), nullable=True))
    op.add_column('task', sa.Column('creation_date', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('creation_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'creation_date')
    op.drop_column('task', 'creation_date')
    op.drop_column('product', 'creation_date')
    op.drop_column('planogram', 'creation_date')
    op.drop_column('customer', 'creation_date')
    op.drop_column('company', 'creation_date')
    op.drop_column('agent', 'creation_date')
    # ### end Alembic commands ###