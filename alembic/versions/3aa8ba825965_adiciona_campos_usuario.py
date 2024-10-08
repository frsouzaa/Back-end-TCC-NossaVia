"""adiciona campos usuario

Revision ID: 3aa8ba825965
Revises: 951fd4d564ad
Create Date: 2024-09-09 23:08:54.248222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from src.db.database import Sexo


# revision identifiers, used by Alembic.
revision: str = '3aa8ba825965'
down_revision: Union[str, None] = '951fd4d564ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    post_status = postgresql.ENUM(Sexo, name="sexo")
    post_status.create(op.get_bind(), checkfirst=True)
    op.add_column('usuario', sa.Column('sexo',  post_status, nullable=False))
    op.add_column('usuario', sa.Column('telefone', sa.String(length=20), nullable=False))
    op.alter_column('usuario', 'numero_endereco',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    op.alter_column('usuario', 'complemento_endereco',
               existing_type=sa.VARCHAR(length=200),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('usuario', 'complemento_endereco',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    op.alter_column('usuario', 'numero_endereco',
               existing_type=sa.VARCHAR(length=200),
               nullable=False)
    op.drop_column('usuario', 'telefone')
    op.drop_column('usuario', 'sexo')
    post_status = postgresql.ENUM(Sexo, name="sexo")
    post_status.drop(op.get_bind())
    # ### end Alembic commands ###
