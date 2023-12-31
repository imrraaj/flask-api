"""added Reward enum

Revision ID: b3dbcfcc495a
Revises: aea530fdc5fc
Create Date: 2023-07-28 15:55:25.890392

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b3dbcfcc495a'
down_revision = 'aea530fdc5fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reward', schema=None) as batch_op:
        batch_op.add_column(sa.Column('used_on', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('status', sa.Enum('NOT_REDEEMED', 'REDEEMED', 'EXPIRED', name='rewardstatus'), nullable=True))
        batch_op.alter_column('expiry_date',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.drop_column('used')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reward', schema=None) as batch_op:
        batch_op.add_column(sa.Column('used', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
        batch_op.alter_column('expiry_date',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.drop_column('status')
        batch_op.drop_column('used_on')

    # ### end Alembic commands ###
