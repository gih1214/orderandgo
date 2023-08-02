"""empty message

Revision ID: d0dc02d2e8ba
Revises: 743ed375c49f
Create Date: 2023-08-03 01:28:34.902140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0dc02d2e8ba'
down_revision = '743ed375c49f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.add_column(sa.Column('page', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('position', sa.Integer(), nullable=True))

    with op.batch_alter_table('menu_option', schema=None) as batch_op:
        batch_op.add_column(sa.Column('page', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('position', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('menu_option', schema=None) as batch_op:
        batch_op.drop_column('position')
        batch_op.drop_column('page')

    with op.batch_alter_table('menu', schema=None) as batch_op:
        batch_op.drop_column('position')
        batch_op.drop_column('page')

    # ### end Alembic commands ###
