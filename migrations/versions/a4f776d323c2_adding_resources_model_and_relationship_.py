"""Adding resources model and relationship to user

Revision ID: a4f776d323c2
Revises: 4cffaa7ed046
Create Date: 2023-12-02 13:12:13.693068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4f776d323c2'
down_revision = '4cffaa7ed046'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resources',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('resource', sa.String(length=200), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('resources', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_resources_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_resources_modified_at'), ['modified_at'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resources', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_resources_modified_at'))
        batch_op.drop_index(batch_op.f('ix_resources_created_at'))

    op.drop_table('resources')
    # ### end Alembic commands ###
