"""Add Referer model

Revision ID: 60b43c4a8bed
Revises: 480b4604ec7a
Create Date: 2022-12-26 18:34:36.049504

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "60b43c4a8bed"
down_revision = "480b4604ec7a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "referer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("referer_value", sa.String(length=4096), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("url_view", schema=None) as batch_op:
        batch_op.add_column(sa.Column("referer_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, "referer", ["referer_id"], ["id"])

    with op.batch_alter_table("user_agent", schema=None) as batch_op:
        batch_op.alter_column(
            "user_agent_value",
            existing_type=sa.VARCHAR(length=250),
            type_=sa.String(length=4096),
            existing_nullable=False,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user_agent", schema=None) as batch_op:
        batch_op.alter_column(
            "user_agent_value",
            existing_type=sa.String(length=4096),
            type_=sa.VARCHAR(length=250),
            existing_nullable=False,
        )

    with op.batch_alter_table("url_view", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.drop_column("referer_id")

    op.drop_table("referer")
    # ### end Alembic commands ###
