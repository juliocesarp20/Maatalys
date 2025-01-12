"""Add search and parameter_search models

Revision ID: d55f67c9531d
Revises: 
Create Date: 2025-01-11 18:33:39.136041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd55f67c9531d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parameter',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('investigation',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_investigation_id'), 'investigation', ['id'], unique=False)
    op.create_table('search',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('investigation_id', sa.UUID(), nullable=False),
    sa.Column('source', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['investigation_id'], ['investigation.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('parameter_search',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('search_id', sa.UUID(), nullable=False),
    sa.Column('parameter_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['parameter_id'], ['parameter.id'], ),
    sa.ForeignKeyConstraint(['search_id'], ['search.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parameter_search')
    op.drop_table('search')
    op.drop_index(op.f('ix_investigation_id'), table_name='investigation')
    op.drop_table('investigation')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('parameter')
    # ### end Alembic commands ###
