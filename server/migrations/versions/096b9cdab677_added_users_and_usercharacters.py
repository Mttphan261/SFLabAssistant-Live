"""added users and usercharacters

Revision ID: 096b9cdab677
Revises: bb15d27fd0f8
Create Date: 2023-07-07 13:20:35.695393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '096b9cdab677'
down_revision = 'bb15d27fd0f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_password_hash', sa.String(), nullable=False))
        batch_op.drop_column('_User__password_hash')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_User__password_hash', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('_password_hash')

    # ### end Alembic commands ###
