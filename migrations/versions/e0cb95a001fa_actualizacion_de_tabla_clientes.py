"""actualizacion de tabla clientes

Revision ID: e0cb95a001fa
Revises: 23d2bc482479
Create Date: 2025-04-13 12:39:18.944186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0cb95a001fa'
down_revision = '23d2bc482479'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('job_title', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.drop_column('job_title')

    # ### end Alembic commands ###
