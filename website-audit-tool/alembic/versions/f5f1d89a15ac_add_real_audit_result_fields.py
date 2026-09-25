"""add real audit result fields

Revision ID: f5f1d89a15ac
Revises:
Create Date: 2026-08-13
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ============================================================
# REVISION IDENTIFIERS
# ============================================================

revision: str = "f5f1d89a15ac"

down_revision: Union[str, Sequence[str], None] = None

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None


# ============================================================
# UPGRADE
# ============================================================

def upgrade() -> None:
    """
    Upgrade the existing audits table safely.

    IMPORTANT:
    Existing audit rows already exist in SQLite.

    Therefore new NOT NULL columns cannot be added directly
    without first providing values for existing rows.
    """

    # --------------------------------------------------------
    # 1. Add status safely
    # --------------------------------------------------------

    op.add_column(
        "audits",
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
            server_default="completed",
        ),
    )

    # --------------------------------------------------------
    # 2. Add error information
    # --------------------------------------------------------

    op.add_column(
        "audits",
        sa.Column(
            "error_message",
            sa.Text(),
            nullable=True,
        ),
    )

    # --------------------------------------------------------
    # 3. Add audit duration
    # --------------------------------------------------------

    op.add_column(
        "audits",
        sa.Column(
            "duration_seconds",
            sa.Float(),
            nullable=True,
        ),
    )

    # --------------------------------------------------------
    # 4. Add SEO metrics
    #
    # Existing audits receive {}.
    # --------------------------------------------------------

    op.add_column(
        "audits",
        sa.Column(
            "seo_metrics",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'"),
        ),
    )

    # --------------------------------------------------------
    # 5. Add Lighthouse / performance metrics
    # --------------------------------------------------------

    op.add_column(
        "audits",
        sa.Column(
            "performance_metrics",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'"),
        ),
    )

    # --------------------------------------------------------
    # 6. Add UI/UX score
    # --------------------------------------------------------

    op.add_column(
        "audits",
        sa.Column(
            "uiux_score",
            sa.Float(),
            nullable=True,
        ),
    )

    # --------------------------------------------------------
    # 7. Add UI/UX metrics
    # --------------------------------------------------------

    op.add_column(
        "audits",
        sa.Column(
            "uiux_metrics",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'"),
        ),
    )

    # --------------------------------------------------------
    # 8. Add page details
    # --------------------------------------------------------

    op.add_column(
        "audits",
        sa.Column(
            "page_details",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'"),
        ),
    )

    # --------------------------------------------------------
    # 9. Add completion timestamp
    # --------------------------------------------------------

    op.add_column(
        "audits",
        sa.Column(
            "completed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    # --------------------------------------------------------
    # 10. Remove temporary database defaults
    #
    # The SQLAlchemy model owns the application defaults.
    # We only needed server defaults during migration to
    # populate existing rows safely.
    # --------------------------------------------------------

    with op.batch_alter_table("audits") as batch_op:

        batch_op.alter_column(
            "status",
            server_default=None,
        )

        batch_op.alter_column(
            "seo_metrics",
            server_default=None,
        )

        batch_op.alter_column(
            "performance_metrics",
            server_default=None,
        )

        batch_op.alter_column(
            "uiux_metrics",
            server_default=None,
        )

        batch_op.alter_column(
            "page_details",
            server_default=None,
        )

        # ----------------------------------------------------
        # Existing score columns must allow NULL.
        # ----------------------------------------------------

        batch_op.alter_column(
            "seo_score",
            existing_type=sa.Float(),
            nullable=True,
        )

        batch_op.alter_column(
            "performance_score",
            existing_type=sa.Float(),
            nullable=True,
        )

        batch_op.alter_column(
            "accessibility_score",
            existing_type=sa.Float(),
            nullable=True,
        )

        batch_op.alter_column(
            "security_score",
            existing_type=sa.Float(),
            nullable=True,
        )

        batch_op.alter_column(
            "mobile_score",
            existing_type=sa.Float(),
            nullable=True,
        )

        batch_op.alter_column(
            "overall_score",
            existing_type=sa.Float(),
            nullable=True,
        )

        batch_op.alter_column(
            "grade",
            existing_type=sa.String(length=4),
            nullable=True,
        )

        batch_op.alter_column(
            "summary",
            existing_type=sa.Text(),
            nullable=True,
        )


# ============================================================
# DOWNGRADE
# ============================================================

def downgrade() -> None:
    """
    Reverse the audit schema migration.
    """

    with op.batch_alter_table("audits") as batch_op:

        batch_op.drop_column("completed_at")
        batch_op.drop_column("page_details")
        batch_op.drop_column("uiux_metrics")
        batch_op.drop_column("uiux_score")
        batch_op.drop_column("performance_metrics")
        batch_op.drop_column("seo_metrics")
        batch_op.drop_column("duration_seconds")
        batch_op.drop_column("error_message")
        batch_op.drop_column("status")

        # Restore original NOT NULL constraints.

        batch_op.alter_column(
            "seo_score",
            existing_type=sa.Float(),
            nullable=False,
        )

        batch_op.alter_column(
            "performance_score",
            existing_type=sa.Float(),
            nullable=False,
        )

        batch_op.alter_column(
            "accessibility_score",
            existing_type=sa.Float(),
            nullable=False,
        )

        batch_op.alter_column(
            "security_score",
            existing_type=sa.Float(),
            nullable=False,
        )

        batch_op.alter_column(
            "mobile_score",
            existing_type=sa.Float(),
            nullable=False,
        )

        batch_op.alter_column(
            "overall_score",
            existing_type=sa.Float(),
            nullable=False,
        )

        batch_op.alter_column(
            "grade",
            existing_type=sa.String(length=4),
            nullable=False,
        )

        batch_op.alter_column(
            "summary",
            existing_type=sa.Text(),
            nullable=False,
        )