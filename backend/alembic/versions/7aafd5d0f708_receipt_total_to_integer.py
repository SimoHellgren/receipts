"""receipt total to integer amount of cents

Revision ID: 7aafd5d0f708
Revises: c8f92f9fbf6d
Create Date: 2021-10-26 21:06:08.624207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7aafd5d0f708'
down_revision = 'c8f92f9fbf6d'
branch_labels = None
depends_on = None


def upgrade():
    # Before changing column type, multiply values by 100 in order to turn euros into cents
    # In case there are floating point inaccuracies, this should truncate correctly
    op.execute('''UPDATE receipt SET total = total * 100''')
    
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('receipt', 'total',
               existing_type=sa.NUMERIC(),
               type_=sa.Integer(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('receipt', 'total',
               existing_type=sa.Integer(),
               type_=sa.NUMERIC(),
               existing_nullable=True)
    # ### end Alembic commands ###

    # divide by 100 to get correct number
    op.execute('''UPDATE receipt SET total = round(total / 100, 2)''')