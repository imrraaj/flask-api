"""birthday

Revision ID: d61d9f9106b8
Revises: d91c878dc2bf
Create Date: 2023-07-31 20:16:19.052897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd61d9f9106b8'
down_revision = 'd91c878dc2bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('birth_date', sa.Date(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('birth_date')

    # ### end Alembic commands ###