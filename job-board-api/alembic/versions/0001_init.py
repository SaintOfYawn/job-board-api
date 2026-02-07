"""init

Revision ID: 0001_init
Revises:
Create Date: 2026-02-07
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_role = sa.Enum("user", "company", "admin", name="user_role")
    employment_type = sa.Enum("full_time", "part_time", "contract", "internship", name="employment_type")

    user_role.create(op.get_bind(), checkfirst=True)
    employment_type.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=2000), nullable=True),
        sa.Column("website", sa.String(length=300), nullable=True),
        sa.Column("owner_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
    )
    op.create_index("ix_companies_name", "companies", ["name"], unique=False)
    op.create_index("ix_companies_owner_user_id", "companies", ["owner_user_id"], unique=True)

    op.create_table(
        "vacancies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=6000), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=True),
        sa.Column("min_salary", sa.Integer(), nullable=True),
        sa.Column("max_salary", sa.Integer(), nullable=True),
        sa.Column("employment_type", employment_type, nullable=False, server_default="full_time"),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_index("ix_vacancies_title", "vacancies", ["title"], unique=False)
    op.create_index("ix_vacancies_company_id", "vacancies", ["company_id"], unique=False)

    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("cover_letter", sa.String(length=3000), nullable=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("vacancy_id", sa.Integer(), sa.ForeignKey("vacancies.id", ondelete="CASCADE"), nullable=False),
        sa.UniqueConstraint("user_id", "vacancy_id", name="uq_user_vacancy_application"),
    )
    op.create_index("ix_applications_user_id", "applications", ["user_id"], unique=False)
    op.create_index("ix_applications_vacancy_id", "applications", ["vacancy_id"], unique=False)


def downgrade() -> None:
    op.drop_table("applications")
    op.drop_table("vacancies")
    op.drop_table("companies")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    sa.Enum(name="employment_type").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="user_role").drop(op.get_bind(), checkfirst=True)
