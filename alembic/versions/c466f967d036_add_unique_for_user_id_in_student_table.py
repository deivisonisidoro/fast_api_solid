"""add unique for user id in Student table

Revision ID: c466f967d036
Revises: 42edc71a1b64
Create Date: 2023-03-12 16:15:52.717199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c466f967d036'
down_revision = '42edc71a1b64'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'students', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'students', type_='unique')
    # ### end Alembic commands ###
