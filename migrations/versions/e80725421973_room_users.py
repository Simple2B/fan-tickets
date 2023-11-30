"""room_users

Revision ID: e80725421973
Revises: 74811d52a2d0
Create Date: 2023-11-30 14:44:52.301927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e80725421973'
down_revision = '74811d52a2d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rooms', schema=None) as batch_op:
        batch_op.alter_column('seller_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('buyer_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rooms', schema=None) as batch_op:
        batch_op.alter_column('buyer_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('seller_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
