"""empty message

Revision ID: ae08c4ba964c
Revises: 820fd25ff62b
Create Date: 2021-08-07 13:29:22.690077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae08c4ba964c'
down_revision = '820fd25ff62b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('owner', sa.String(), nullable=False))
    op.drop_constraint('characters_user_token_fkey', 'characters', type_='foreignkey')
    op.create_foreign_key(None, 'characters', 'user', ['owner'], ['token'])
    op.drop_column('characters', 'owner')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('user_token', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'characters', type_='foreignkey')
    op.create_foreign_key('characters_user_token_fkey', 'characters', 'user', ['user_token'], ['token'])
    op.drop_column('characters', 'owner')
    # ### end Alembic commands ###