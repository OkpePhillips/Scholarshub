"""creating new models

Revision ID: c4039891257d
Revises: 3dac510ffc87
Create Date: 2023-11-28 11:16:35.586196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4039891257d'
down_revision = '3dac510ffc87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('region', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_region_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_region_modified_at'), ['modified_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_region_timestamp'), ['timestamp'], unique=False)

    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('completed_status', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_service_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_service_modified_at'), ['modified_at'], unique=False)

    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=1024), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['region_id'], ['region.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_post_modified_at'), ['modified_at'], unique=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('modified_at', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_modified_at'), ['modified_at'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_modified_at'))
        batch_op.drop_index(batch_op.f('ix_user_created_at'))
        batch_op.drop_column('modified_at')
        batch_op.drop_column('created_at')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_modified_at'))
        batch_op.drop_index(batch_op.f('ix_post_created_at'))

    op.drop_table('post')
    with op.batch_alter_table('service', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_service_modified_at'))
        batch_op.drop_index(batch_op.f('ix_service_created_at'))

    op.drop_table('service')
    with op.batch_alter_table('region', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_region_timestamp'))
        batch_op.drop_index(batch_op.f('ix_region_modified_at'))
        batch_op.drop_index(batch_op.f('ix_region_created_at'))

    op.drop_table('region')
    # ### end Alembic commands ###
