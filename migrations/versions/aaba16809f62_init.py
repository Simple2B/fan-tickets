"""init

Revision ID: aaba16809f62
Revises: 8636665466e1
Create Date: 2023-11-22 13:17:07.961874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaba16809f62'
down_revision = '8636665466e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('picture_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('picture_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
