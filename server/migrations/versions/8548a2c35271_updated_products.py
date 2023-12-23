"""updated products

Revision ID: 8548a2c35271
Revises: 7d420d6660e1
Create Date: 2023-12-20 17:24:07.424155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8548a2c35271'
down_revision = '7d420d6660e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
