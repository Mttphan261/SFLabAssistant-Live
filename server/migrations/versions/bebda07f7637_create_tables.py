"""create tables

Revision ID: bebda07f7637
Revises: 
Create Date: 2023-07-26 15:39:51.595500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bebda07f7637'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('head_img', sa.String(), nullable=True),
    sa.Column('main_img', sa.String(), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_characters'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('_password_hash', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email')),
    sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    op.create_table('combos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('notation', sa.String(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_combos_character_id_characters')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_combos'))
    )
    op.create_table('moves',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('command', sa.String(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_moves_character_id_characters')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_moves'))
    )
    op.create_table('user_characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_main', sa.Boolean(), nullable=True),
    sa.Column('is_alt', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_user_characters_character_id_characters')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_characters_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_characters')),
    sa.UniqueConstraint('user_id', 'character_id', name='_user_character_uc')
    )
    op.create_table('matchups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('user_character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_character_id'], ['user_characters.id'], name=op.f('fk_matchups_user_character_id_user_characters')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_matchups'))
    )
    op.create_table('training_notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('note', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_character_id'], ['user_characters.id'], name=op.f('fk_training_notes_user_character_id_user_characters')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_training_notes_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_training_notes'))
    )
    op.create_table('videos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('video_id', sa.String(), nullable=True),
    sa.Column('embed_html', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], name=op.f('fk_videos_character_id_characters')),
    sa.ForeignKeyConstraint(['user_character_id'], ['user_characters.id'], name=op.f('fk_videos_user_character_id_user_characters')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_videos_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_videos'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('videos')
    op.drop_table('training_notes')
    op.drop_table('matchups')
    op.drop_table('user_characters')
    op.drop_table('moves')
    op.drop_table('combos')
    op.drop_table('users')
    op.drop_table('characters')
    # ### end Alembic commands ###
