"""empty message

Revision ID: e6068e4a8417
Revises: 169b2d5bb300
Create Date: 2020-07-29 12:21:32.701179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6068e4a8417'
down_revision = '169b2d5bb300'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_company'))
    )
    op.add_column('customer', sa.Column('company_id', sa.Integer(), nullable=True))
    op.drop_constraint('fk_customer_user_id_user', 'customer', type_='foreignkey')
    op.create_foreign_key(op.f('fk_customer_company_id_company'), 'customer', 'company', ['company_id'], ['id'])
    op.drop_column('customer', 'user_id')
    op.add_column('user', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_user_company_id_company'), 'user', 'company', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_user_company_id_company'), 'user', type_='foreignkey')
    op.drop_column('user', 'company_id')
    op.add_column('customer', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(op.f('fk_customer_company_id_company'), 'customer', type_='foreignkey')
    op.create_foreign_key('fk_customer_user_id_user', 'customer', 'user', ['user_id'], ['id'])
    op.drop_column('customer', 'company_id')
    op.drop_table('company')
    # ### end Alembic commands ###
