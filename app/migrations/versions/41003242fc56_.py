"""empty message

Revision ID: 41003242fc56
Revises: accd59b912bf
Create Date: 2020-08-07 17:48:16.287846

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41003242fc56'
down_revision = 'accd59b912bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('agent', 'image',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=150),
               existing_nullable=True)
    op.alter_column('planogram', 'image',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=150),
               existing_nullable=True)
    op.alter_column('product', 'image',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=150),
               existing_nullable=True)
    op.alter_column('user', 'profile_image',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=150),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'profile_image',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    op.alter_column('product', 'image',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    op.alter_column('planogram', 'image',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    op.alter_column('agent', 'image',
               existing_type=sa.String(length=150),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###