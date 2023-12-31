"""Adding more fields to post table as necessary

Revision ID: e0be721750b8
Revises: 6f7d7871c4e6
Create Date: 2023-11-29 13:49:29.610869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e0be721750b8'
down_revision = '6f7d7871c4e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('requirements', sa.String(length=500), nullable=False))
        batch_op.add_column(sa.Column('how_to_apply', sa.String(length=500), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('how_to_apply')
        batch_op.drop_column('requirements')

    # ### end Alembic commands ###
