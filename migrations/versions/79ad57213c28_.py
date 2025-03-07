"""empty message

Revision ID: 79ad57213c28
Revises: 5d1366e3798b
Create Date: 2023-09-13 16:52:28.012021

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '79ad57213c28'
down_revision = '5d1366e3798b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('store', schema=None) as batch_op:
        batch_op.alter_column('store_pw',
               existing_type=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=50),
               type_=sa.String(length=120),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('store', schema=None) as batch_op:
        batch_op.alter_column('store_pw',
               existing_type=sa.String(length=120),
               type_=mysql.VARCHAR(charset='utf8mb4', collation='utf8mb4_0900_ai_ci', length=50),
               existing_nullable=False)

    # ### end Alembic commands ###
