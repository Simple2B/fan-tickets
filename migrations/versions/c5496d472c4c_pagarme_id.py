"""pagarme_id

Revision ID: c5496d472c4c
Revises: 9d07ac169469
Create Date: 2023-12-26 15:26:17.010038

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5496d472c4c'
down_revision = '9d07ac169469'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pagarme_id', sa.String(length=32), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('pagarme_id')

    # ### end Alembic commands ###
