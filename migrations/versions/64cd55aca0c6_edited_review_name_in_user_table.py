"""Edited review name in user table

Revision ID: 64cd55aca0c6
Revises: f489c4e3cc51
Create Date: 2023-12-07 15:51:27.126568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64cd55aca0c6'
down_revision = 'f489c4e3cc51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reviewed', sa.String(length=255), nullable=True))
        batch_op.drop_column('reviewed_cv')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reviewed_cv', sa.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('reviewed')

    # ### end Alembic commands ###
