"""2020_02_18

Revision ID: 000001
Revises: 
Create Date: 2020-02-18 03:57:38.958091

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '000001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('added_on', sa.DateTime(), nullable=False),
                    sa.Column('modified_on', sa.DateTime(), nullable=False),
                    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
                    sa.Column('enabled', sa.Boolean(), nullable=False),
                    sa.Column('last_auth_time', sa.DateTime(), nullable=True),
                    sa.Column('username', sa.String(length=32), nullable=False),
                    sa.Column('password_hash', sa.String(length=128), nullable=True),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
                    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('user_accesses',
                    sa.Column('added_on', sa.DateTime(), nullable=False),
                    sa.Column('modified_on', sa.DateTime(), nullable=False),
                    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
                    sa.Column('enabled', sa.Boolean(), nullable=False),
                    sa.Column('ip_address', sa.String(length=15), nullable=False),
                    sa.Column('external_app_id', sa.String(length=15), nullable=False),
                    sa.Column('users_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['users_id'], ['users.id'], name=op.f('fk_user_accesses_users_id_users'),
                                            onupdate='CASCADE', ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_accesses')),
                    sa.UniqueConstraint('users_id', 'ip_address', 'external_app_id',
                                        name=op.f('uq_user_accesses_users_id'))
                    )
    op.create_index(op.f('ix_user_accesses_external_app_id'), 'user_accesses', ['external_app_id'], unique=True)
    op.create_index(op.f('ix_user_accesses_ip_address'), 'user_accesses', ['ip_address'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_accesses_ip_address'), table_name='user_accesses')
    op.drop_index(op.f('ix_user_accesses_external_app_id'), table_name='user_accesses')
    op.drop_table('user_accesses')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###