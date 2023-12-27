"""identity_document

Revision ID: 56e569105aae
Revises: 9d07ac169469
Create Date: 2023-12-21 11:59:10.495060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56e569105aae'
down_revision = '9d07ac169469'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('identity_document_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('name', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('last_name', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('address', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('birth_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('facebook', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('instagram', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('twitter', sa.String(length=256), nullable=True))
        batch_op.drop_constraint('uq_users_username', type_='unique')
        batch_op.create_unique_constraint(batch_op.f('uq_users_email'), ['email'])
        batch_op.create_foreign_key(batch_op.f('fk_users_identity_document_id_pictures'), 'pictures', ['identity_document_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_users_identity_document_id_pictures'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('uq_users_email'), type_='unique')
        batch_op.create_unique_constraint('uq_users_username', ['username'])
        batch_op.drop_column('twitter')
        batch_op.drop_column('instagram')
        batch_op.drop_column('facebook')
        batch_op.drop_column('birth_date')
        batch_op.drop_column('address')
        batch_op.drop_column('last_name')
        batch_op.drop_column('name')
        batch_op.drop_column('identity_document_id')

    # ### end Alembic commands ###
