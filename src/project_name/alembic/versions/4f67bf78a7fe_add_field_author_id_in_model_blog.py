"""add field author_id in model Blog

Revision ID: 4f67bf78a7fe
Revises: b5492ba60bac
Create Date: 2023-04-13 19:02:28.348065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f67bf78a7fe'
down_revision = 'b5492ba60bac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blog', sa.Column('author_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'blog', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'blog', type_='foreignkey')
    op.drop_column('blog', 'author_id')
    # ### end Alembic commands ###
