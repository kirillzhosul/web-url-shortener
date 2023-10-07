"""Add TimestampMixin for tables

Revision ID: bdd69a039098
Revises: 7ab4d082ce9b
Create Date: 2023-01-04 18:53:15.648469

Copyright (C) 2022-2023 Stepan Zubkov <stepanzubkov@florgon.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "bdd69a039098"
down_revision = "7ab4d082ce9b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("url_views", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_at", sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=False))
        batch_op.drop_column("view_date")

    with op.batch_alter_table("urls", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_at", sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("urls", schema=None) as batch_op:
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    with op.batch_alter_table("url_views", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "view_date", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
            )
        )
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    # ### end Alembic commands ###
