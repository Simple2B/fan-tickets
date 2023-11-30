"""room_ticket

Revision ID: 9a3d8be41d15
Revises: e80725421973
Create Date: 2023-11-30 14:57:18.316460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a3d8be41d15'
down_revision = 'e80725421973'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rooms', schema=None) as batch_op:
        batch_op.alter_column('ticket_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rooms', schema=None) as batch_op:
        batch_op.alter_column('ticket_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
