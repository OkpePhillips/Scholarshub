"""Editing resource relationship

Revision ID: c5c8fc96d6ac
Revises: a4f776d323c2
Create Date: 2023-12-02 14:03:13.255030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5c8fc96d6ac'
down_revision = 'a4f776d323c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resources', schema=None) as batch_op:
        batch_op.add_column(sa.Column('resource', sa.String(length=200), nullable=True))
        batch_op.drop_column('filepath')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resources', schema=None) as batch_op:
        batch_op.add_column(sa.Column('filepath', sa.VARCHAR(length=200), nullable=True))
        batch_op.drop_column('resource')

    # ### end Alembic commands ###