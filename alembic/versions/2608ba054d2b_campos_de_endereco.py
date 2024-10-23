"""campos de endereco

Revision ID: 2608ba054d2b
Revises: 467bd0a507d9
Create Date: 2024-10-18 22:44:34.421513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.db.database import Estado


# revision identifiers, used by Alembic.
revision: str = '2608ba054d2b'
down_revision: Union[str, None] = '467bd0a507d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    status = sa.Enum(Estado, name="estado")
    status.create(op.get_bind(), checkfirst=True)
    op.add_column('reclamacao', sa.Column('bairro', sa.String(length=200), nullable=True))
    op.add_column('reclamacao', sa.Column('cidade', sa.String(length=200), nullable=True))
    op.add_column('reclamacao', sa.Column('estado', sa.Enum('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO', name='estado'), nullable=True))
    op.add_column('usuario', sa.Column('cpf', sa.String(length=50), nullable=False))
    op.add_column('usuario', sa.Column('bairro', sa.String(length=200), nullable=False))
    op.add_column('usuario', sa.Column('cidade', sa.String(length=200), nullable=False))
    op.add_column('usuario', sa.Column('estado', sa.Enum('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO', name='estado'), nullable=False))
    op.create_unique_constraint(None, 'usuario', ['cpf'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'usuario', type_='unique')
    op.drop_column('usuario', 'estado')
    op.drop_column('usuario', 'cidade')
    op.drop_column('usuario', 'bairro')
    op.drop_column('usuario', 'cpf')
    op.drop_column('reclamacao', 'estado')
    op.drop_column('reclamacao', 'cidade')
    op.drop_column('reclamacao', 'bairro')
    status = sa.Enum(Estado, name="estado")
    status.drop(op.get_bind())
    # ### end Alembic commands ###