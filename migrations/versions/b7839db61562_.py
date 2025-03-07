"""empty message

Revision ID: b7839db61562
Revises: c613199f7703
Create Date: 2023-10-18 19:53:57.398149

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b7839db61562'
down_revision = 'c613199f7703'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.alter_column('menu_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
        batch_op.alter_column('table_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    with op.batch_alter_table('table_order_list', schema=None) as batch_op:
        batch_op.alter_column('table_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    with op.batch_alter_table('table_payment_list', schema=None) as batch_op:
        batch_op.drop_constraint('store_id', type_='unique')
        batch_op.drop_index('store_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('table_payment_list', schema=None) as batch_op:
        batch_op.create_index('store_id', ['store_id', 'table_id', 'first_order_time'], unique=False)
        batch_op.create_unique_constraint('store_id', ['store_id', 'table_id', 'first_order_time'])

    with op.batch_alter_table('table_order_list', schema=None) as batch_op:
        batch_op.alter_column('table_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.alter_column('table_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
        batch_op.alter_column('menu_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
