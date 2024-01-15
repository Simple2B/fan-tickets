"""add payload to notification

Revision ID: 3821be89c96b
Revises: 6a21d8e49b0b
Create Date: 2024-01-12 13:20:29.994045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3821be89c96b'
down_revision = '6a21d8e49b0b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('payload', sa.JSON(), nullable=False))
        batch_op.drop_column('text')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('text', sa.VARCHAR(length=512), autoincrement=False, nullable=False))
        batch_op.drop_column('payload')

    # ### end Alembic commands ###