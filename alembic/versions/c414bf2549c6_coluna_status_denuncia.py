"""coluna status denuncia

Revision ID: 73e344246bea
Revises: 1a3b4b737666
Create Date: 2024-10-02 22:17:08.880017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.db.database import Status


# revision identifiers, used by Alembic.
revision: str = '73e344246bea'
down_revision: Union[str, None] = '1a3b4b737666'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    status = sa.Enum(Status, name="status")
    status.create(op.get_bind(), checkfirst=True)
    op.add_column('denuncia', sa.Column('status', sa.Enum('resolvido', 'nao_resolvido', name='status'), nullable=False))
    op.add_column('denuncia', sa.Column('atualizacao_status', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('denuncia', 'atualizacao_status')
    op.drop_column('denuncia', 'status')
    status = sa.Enum(Status, name="status")
    status.drop(op.get_bind())
    # ### end Alembic commands ###
