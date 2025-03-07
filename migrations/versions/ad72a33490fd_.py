"""empty message

Revision ID: ad72a33490fd
Revises: 
Create Date: 2023-08-03 18:37:34.858334

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ad72a33490fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.alter_column('store_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('menu_category_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.alter_column('menu_category_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('store_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
