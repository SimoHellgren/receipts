"""initial migration

Revision ID: c8f92f9fbf6d
Revises: 
Create Date: 2021-10-12 18:35:57.702469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8f92f9fbf6d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chain',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('paymentmethod',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('payer', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('chain_id', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['chain_id'], ['chain.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receipt',
    sa.Column('id', sa.Text(), nullable=False),
    sa.Column('reprint', sa.Text(), nullable=True),
    sa.Column('total', sa.Numeric(), nullable=True),
    sa.Column('etag', sa.Text(), nullable=True),
    sa.Column('datetime', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('store_id', sa.Text(), nullable=True),
    sa.Column('paymentmethod_id', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['paymentmethod_id'], ['paymentmethod.id'], ),
    sa.ForeignKeyConstraint(['store_id'], ['store.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receiptline',
    sa.Column('receipt_id', sa.Text(), nullable=False),
    sa.Column('linenumber', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Text(), nullable=True),
    sa.Column('amount', sa.Numeric(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['receipt_id'], ['receipt.id'], ),
    sa.PrimaryKeyConstraint('receipt_id', 'linenumber')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('receiptline')
    op.drop_table('receipt')
    op.drop_table('store')
    op.drop_table('product')
    op.drop_table('paymentmethod')
    op.drop_table('chain')
    # ### end Alembic commands ###
