"""empty message

Revision ID: e5fe2648104a
Revises: 5fa9c75f922b
Create Date: 2016-11-08 23:34:38.423021

"""

# revision identifiers, used by Alembic.
revision = 'e5fe2648104a'
down_revision = '5fa9c75f922b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_item', 'comment',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.String(length=2048),
               existing_nullable=True)
    op.alter_column('order_item', 'url',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.String(length=2048),
               existing_nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('order_item', 'url',
               existing_type=sa.String(length=2048),
               type_=sa.VARCHAR(length=256),
               existing_nullable=False)
    op.alter_column('order_item', 'comment',
               existing_type=sa.String(length=2048),
               type_=sa.VARCHAR(length=256),
               existing_nullable=True)
    ### end Alembic commands ###
