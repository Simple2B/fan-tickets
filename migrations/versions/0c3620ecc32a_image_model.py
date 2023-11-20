"""image_model

Revision ID: 0c3620ecc32a
Revises: 865939effd41
Create Date: 2023-11-20 12:47:38.396026

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0c3620ecc32a'
down_revision = '865939effd41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pictures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=256), nullable=False),
    sa.Column('mimetype', sa.String(length=32), nullable=False),
    sa.Column('file', sa.LargeBinary(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_pictures'))
    )
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_categories_picture_id_pictures'), 'pictures', ['picture_id'], ['id'])
        batch_op.drop_column('image')

    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_events_picture_id_pictures'), 'pictures', ['picture_id'], ['id'])
        batch_op.drop_column('image')

    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_locations_picture_id_pictures'), 'pictures', ['picture_id'], ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_users_picture_id_pictures'), 'pictures', ['picture_id'], ['id'])
        batch_op.drop_column('image')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', postgresql.BYTEA(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_users_picture_id_pictures'), type_='foreignkey')
        batch_op.drop_column('picture_id')

    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_locations_picture_id_pictures'), type_='foreignkey')
        batch_op.drop_column('picture_id')

    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', postgresql.BYTEA(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_events_picture_id_pictures'), type_='foreignkey')
        batch_op.drop_column('picture_id')

    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', postgresql.BYTEA(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_categories_picture_id_pictures'), type_='foreignkey')
        batch_op.drop_column('picture_id')

    op.drop_table('pictures')
    # ### end Alembic commands ###
