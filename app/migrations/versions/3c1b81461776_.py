"""empty message

Revision ID: 3c1b81461776
Revises: 170581f68fb7
Create Date: 2020-07-16 21:37:18.853130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c1b81461776'
down_revision = '170581f68fb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('mobile_number', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=40), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(length=40), nullable=True),
    sa.Column('street_name', sa.String(length=40), nullable=False),
    sa.Column('postal_code', sa.String(length=10), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], name=op.f('fk_customer_country_id_country')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_customer'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('customer')
    # ### end Alembic commands ###
