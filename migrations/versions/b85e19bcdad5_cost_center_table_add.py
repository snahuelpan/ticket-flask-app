"""cost_center table add

Revision ID: b85e19bcdad5
Revises: a6d42d567e41
Create Date: 2025-04-13 22:46:27.031365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b85e19bcdad5'
down_revision = 'a6d42d567e41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cost_center',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(length=300), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('id_number', sa.Integer(), nullable=True),
    sa.Column('branch', sa.String(length=300), nullable=True),
    sa.Column('location', sa.String(length=300), nullable=True),
    sa.Column('management', sa.String(length=300), nullable=True),
    sa.Column('manager', sa.String(length=300), nullable=True),
    sa.Column('email_manager', sa.String(length=120), nullable=True),
    sa.Column('administrator', sa.String(length=300), nullable=True),
    sa.Column('administrator_email', sa.String(length=300), nullable=True),
    sa.Column('administrator_cellphone', sa.String(length=16), nullable=True),
    sa.Column('active', sa.Integer(), server_default=sa.text('1'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_number')
    )
    with op.batch_alter_table('cost_center', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_cost_center_branch'), ['branch'], unique=True)
        batch_op.create_index(batch_op.f('ix_cost_center_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_cost_center_uuid'), ['uuid'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cost_center', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_cost_center_uuid'))
        batch_op.drop_index(batch_op.f('ix_cost_center_name'))
        batch_op.drop_index(batch_op.f('ix_cost_center_branch'))

    op.drop_table('cost_center')
    # ### end Alembic commands ###
