"""added status

Revision ID: 25d3a531436a
Revises: 6a43ebdd6b19
Create Date: 2023-07-26 20:23:20.959651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25d3a531436a'
down_revision = '6a43ebdd6b19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Enum('ORDERED', 'CANCELLED', 'PAID', 'DELIVERY', name='orderstatus'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###