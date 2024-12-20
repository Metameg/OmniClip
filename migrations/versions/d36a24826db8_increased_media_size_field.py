"""increased media size field

Revision ID: d36a24826db8
Revises: 0668f5efa529
Create Date: 2024-03-21 12:51:05.179412

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd36a24826db8'
down_revision = '0668f5efa529'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('medias', schema=None) as batch_op:
        batch_op.alter_column('size',
               existing_type=mysql.VARCHAR(length=25),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('medias', schema=None) as batch_op:
        batch_op.alter_column('size',
               existing_type=sa.Integer(),
               type_=mysql.VARCHAR(length=25),
               existing_nullable=True)

    # ### end Alembic commands ###
