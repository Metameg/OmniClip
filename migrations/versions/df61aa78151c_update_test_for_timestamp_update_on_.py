"""update test for timestamp update on renders

Revision ID: df61aa78151c
Revises: 82d77b41838e
Create Date: 2024-09-22 21:37:47.157814

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'df61aa78151c'
down_revision = '82d77b41838e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('renders', schema=None) as batch_op:
        batch_op.alter_column('timestamp',
               existing_type=mysql.DATETIME(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('renders', schema=None) as batch_op:
        batch_op.alter_column('timestamp',
               existing_type=mysql.DATETIME(),
               nullable=True)

    # ### end Alembic commands ###