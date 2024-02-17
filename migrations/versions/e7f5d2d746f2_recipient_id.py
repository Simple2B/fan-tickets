"""recipient_id

Revision ID: e7f5d2d746f2
Revises: 265eeedacedf
Create Date: 2024-02-15 18:32:54.305854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7f5d2d746f2'
down_revision = '265eeedacedf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipient_id', sa.String(length=32), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('recipient_id')

    # ### end Alembic commands ###
