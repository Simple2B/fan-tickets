"""Notification type

Revision ID: aa90da3ad25a
Revises: 3821be89c96b
Create Date: 2024-01-12 15:44:00.176259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa90da3ad25a'
down_revision = '3821be89c96b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('notification_type', sa.String(length=32), nullable=False))
        batch_op.drop_column('type_of')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type_of', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
        batch_op.drop_column('notification_type')

    # ### end Alembic commands ###
