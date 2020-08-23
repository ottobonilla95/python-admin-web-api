"""empty message

Revision ID: bfbd08dc5983
Revises: a5afe184f3e9
Create Date: 2020-07-29 17:28:44.238069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfbd08dc5983'
down_revision = 'a5afe184f3e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('menu_title', sa.String(length=30), nullable=False),
    sa.Column('menu_icon', sa.String(length=40), nullable=True),
    sa.Column('path', sa.String(length=60), nullable=True),
    sa.Column('new_item', sa.Boolean(), nullable=True),
    sa.Column('father_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['father_id'], ['menu_item.id'], name=op.f('fk_menu_item_father_id_menu_item')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_menu_item'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('menu_item')
    # ### end Alembic commands ###