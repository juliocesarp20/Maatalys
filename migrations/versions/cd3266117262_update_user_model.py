"""update user model

Revision ID: cd3266117262
Revises: 530d5c65a6ec
Create Date: 2025-01-22 04:33:22.866983

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "cd3266117262"
down_revision: Union[str, None] = "530d5c65a6ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tb_search",
        sa.Column(
            "dt_created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "tb_search",
        sa.Column("dt_processed", sa.DateTime(timezone=True), nullable=True),
    )
    op.drop_column("tb_search", "dt_processing")
    op.drop_column("tb_search", "dt_creation")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "tb_search",
        sa.Column(
            "dt_creation",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "tb_search",
        sa.Column(
            "dt_processing",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("tb_search", "dt_processed")
    op.drop_column("tb_search", "dt_created")
    # ### end Alembic commands ###
