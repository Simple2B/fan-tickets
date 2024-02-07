"""add_identity_number

Revision ID: bc2cafd82e06
Revises: 42b5769b28c5
Create Date: 2024-02-05 11:28:33.836251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc2cafd82e06'
down_revision = '42b5769b28c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('document_identity_number', sa.String(length=32), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('document_identity_number')

    # ### end Alembic commands ###