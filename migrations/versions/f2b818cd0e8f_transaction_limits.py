"""transaction_limits

Revision ID: f2b818cd0e8f
Revises: 7e524aba2283
Create Date: 2024-03-01 12:32:40.362562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2b818cd0e8f'
down_revision = '7e524aba2283'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('global_fee_settings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('selling_limit', sa.Integer(), server_default='5', nullable=False))
        batch_op.add_column(sa.Column('buying_limit', sa.Integer(), server_default='3', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('global_fee_settings', schema=None) as batch_op:
        batch_op.drop_column('buying_limit')
        batch_op.drop_column('selling_limit')

    # ### end Alembic commands ###
