"""empty message

Revision ID: 16cdefea703a
Revises: None
Create Date: 2016-11-04 12:19:33.086623

"""

# revision identifiers, used by Alembic.
revision = '16cdefea703a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice', sa.Column('is_paid', sa.Boolean()))
    ### end Alembic commands ###

    op.execute('UPDATE "invoice" SET is_paid = false')

    op.alter_column("invoice", "is_paid", nullable=True)


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('invoice', 'is_paid')
    ### end Alembic commands ###
