from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    DateTime,
    String,
    func,
    create_engine,
    Boolean,
    BigInteger,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    Mapped,
    mapped_column,
    relationship,
)
import os
from dotenv import load_dotenv
from dataclasses import dataclass
import enum


load_dotenv()
engine = create_engine(os.getenv("DB_URI"))
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
metadata = Base.metadata


class Sexo(enum.Enum):
    m = "m"
    f = "f"
    n = "n"


@dataclass
class Usuario(Base):
    __tablename__: str = "usuario"

    id: int = Column(BigInteger, primary_key=True)
    criacao: str = Column(DateTime, default=func.now(), nullable=False)
    modificacao: str = Column(DateTime, default=func.now(), nullable=False)
    delete: bool = Column(Boolean, default=False, nullable=False)

    nome: str = Column(String(200), nullable=False)
    email: str = Column(String(200), unique=True, nullable=False)
    senha: str = Column(String(200), nullable=False)
    endereco: str = Column(String(200), nullable=False)
    numero_endereco: str = Column(String(200), nullable=True)
    complemento_endereco: str = Column(String(200), nullable=True)
    cep: str = Column(String(20), nullable=False)
    data_nascimento: str = Column(DateTime, nullable=False)
    sexo: str = Column(Enum(Sexo), nullable=False)
    telefone: str = Column(String(20), nullable=False)
    pontucao: int = Column(BigInteger, default=0, nullable=False)

    def __init__(
        self,
        nome: str,
        email: str,
        senha: str,
        endereco: str,
        numero_endereco: str,
        complemento_endereco: str,
        cep: str,
        data_nascimento: str,
        sexo: str,
        telefone: str,
        pontucao: int,
    ) -> None:
        self.nome = nome
        self.email = email
        self.senha = senha
        self.endereco = endereco
        self.numero_endereco = numero_endereco
        self.complemento_endereco = complemento_endereco
        self.cep = cep
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.telefone = telefone
        self.pontucao = pontucao


class Categoria(enum.Enum):
    via = "via"
    calcada = "calcada"
    iluminacao = "iluminacao"
    lixo = "lixo"
    carro = "carro"
    sinalizacao = "sinalizacao"
    outros = "outros"


@dataclass
class Denuncia(Base):
    __tablename__: str = "denuncia"

    id: int = Column(BigInteger, primary_key=True)
    criacao: str = Column(DateTime, default=func.now(), nullable=False)
    modificacao: str = Column(DateTime, default=func.now(), nullable=False)
    delete: bool = Column(Boolean, default=False, nullable=False)

    titulo: str = Column(String(200), nullable=False)
    descricao: str = Column(String(500), nullable=False)
    categoria: str = Column(Enum(Categoria), nullable=False)
    data: str = Column(DateTime, nullable=False)
    endereco: str = Column(String(200), nullable=True)
    numero_endereco: str = Column(String(200), nullable=True)
    ponto_referencia: str = Column(String(200), nullable=True)
    cep: str = Column(String(20), nullable=True)
    latitude: str = Column(String(200), nullable=False)
    longitude: str = Column(String(200), nullable=False)
    fotos: str = Column(String(2000), nullable=False)
    qtd_curtidas: int = Column(BigInteger, default=0, nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))

    def __init__(
        self,
        titulo: str,
        descricao: str,
        categoria: str,
        data: str,
        endereco: str,
        numero_endereco: str,
        ponto_referencia: str,
        cep: str,
        latitude: str,
        longitude: str,
        fotos: str,
        qtd_curtidas: int,
        usuario_id: int,
    ) -> None:
        self.titulo = titulo
        self.descricao = descricao
        self.categoria = categoria
        self.data = data
        self.endereco = endereco
        self.numero_endereco = numero_endereco
        self.ponto_referencia = ponto_referencia
        self.cep = cep
        self.latitude = latitude
        self.longitude = longitude
        self.fotos = fotos
        self.qtd_curtidas = qtd_curtidas
        self.usuario_id = usuario_id
