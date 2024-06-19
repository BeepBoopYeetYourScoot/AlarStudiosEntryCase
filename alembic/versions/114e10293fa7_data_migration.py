"""data migration

Revision ID: 114e10293fa7
Revises: d29f2fe8fa01
Create Date: 2024-06-19 17:40:25.928550

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import MetaData, Table

from initial_data import TABLENAME_TO_CONTENTS

# revision identifiers, used by Alembic.
revision: str = "114e10293fa7"
down_revision: Union[str, None] = "d29f2fe8fa01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    meta = MetaData()
    meta.reflect(only=tuple(TABLENAME_TO_CONTENTS.keys()), bind=op.get_bind())
    for tablename, data in TABLENAME_TO_CONTENTS.items():
        op.bulk_insert(
            Table(tablename, meta, autoload_with=op.get_bind()), data
        )


def downgrade() -> None:
    for tablename, data in TABLENAME_TO_CONTENTS.items():
        ids = [obj["id"] for obj in data]
        op.execute(f"delete from {tablename} where id in {tuple(ids)}")
