"""verification code user

Revision ID: 35cae73a4ee6
Revises: 44573ea2d682
Create Date: 2023-12-04 17:07:05.366208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35cae73a4ee6'
down_revision = '44573ea2d682'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('verification_code', sa.String(length=6), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('verification_code')

    # ### end Alembic commands ###
