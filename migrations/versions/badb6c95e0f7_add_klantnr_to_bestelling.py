"""Add klantnr to Bestelling

Revision ID: badb6c95e0f7
Revises: 
Create Date: 2025-01-14 14:57:50.133642

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'badb6c95e0f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('bestelling', schema=None) as batch_op:
        batch_op.add_column(sa.Column('klantnr', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_bestelling_klant', 'klant', ['klantnr'], ['klantnr'])

def downgrade():
    with op.batch_alter_table('bestelling', schema=None) as batch_op:
        batch_op.drop_constraint('fk_bestelling_klant', type_='foreignkey')
        batch_op.drop_column('klantnr')
