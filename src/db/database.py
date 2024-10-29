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
    UniqueConstraint,
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    Mapped,
    mapped_column,
    declarative_base,
)
import os
from dataclasses import dataclass
import enum
from geoalchemy2 import Geography

engine = create_engine(os.getenv("DB_URI"), pool_size=20, max_overflow=40)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
metadata = Base.metadata


class Sexo(enum.Enum):
    m = "m"
    f = "f"
    n = "n"


class Estado(enum.Enum):
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"


@dataclass
class Usuario(Base):
    __tablename__: str = "usuario"

    id: int = Column(BigInteger, primary_key=True)
    criacao: str = Column(DateTime, default=func.now(), nullable=False)
    modificacao: str = Column(DateTime, default=func.now(), nullable=False)
    delete: bool = Column(Boolean, default=False, nullable=False)

    nome: str = Column(String(200), nullable=False)
    cpf: str = Column(String(50), unique=True, nullable=False)
    email: str = Column(String(200), unique=True, nullable=False)
    senha: str = Column(String(200), nullable=False)
    cep: str = Column(String(20), nullable=False)
    endereco: str = Column(String(200), nullable=False)
    numero_endereco: str = Column(String(200), nullable=True)
    complemento_endereco: str = Column(String(200), nullable=True)
    bairro: str = Column(String(200), nullable=False)
    cidade: str = Column(String(200), nullable=False)
    estado: str = Column(Enum(Estado), nullable=False)
    data_nascimento: str = Column(DateTime, nullable=False)
    sexo: str = Column(Enum(Sexo), nullable=False)
    telefone: str = Column(String(20), nullable=False)
    pontucao: int = Column(BigInteger, default=0, nullable=False)
    foto: str = Column(String(2000), nullable=True)

    def __init__(
        self,
        nome: str,
        cpf: str,
        email: str,
        senha: str,
        cep: str,
        endereco: str,
        numero_endereco: str,
        complemento_endereco: str,
        bairro: str,
        cidade: str,
        estado: str,
        data_nascimento: str,
        sexo: str,
        telefone: str,
        pontucao: int,
    ) -> None:
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.cep = cep
        self.endereco = endereco
        self.numero_endereco = numero_endereco
        self.complemento_endereco = complemento_endereco
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.telefone = telefone
        self.pontucao = pontucao


class RecuperarSenha(Base):
    __tablename__: str = "recuperar_senha"

    id: int = Column(BigInteger, primary_key=True)
    criacao: str = Column(DateTime, default=func.now(), nullable=False)
    modificacao: str = Column(DateTime, default=func.now(), nullable=False)
    delete: bool = Column(Boolean, default=False, nullable=False)

    token: str = Column(String(200), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))

    def __init__(self, token: str, usuario_id: int) -> None:
        self.token = token
        self.usuario_id = usuario_id


class Categoria(enum.Enum):
    via = "via"
    calcada = "calcada"
    iluminacao = "iluminacao"
    lixo = "lixo"
    carro = "carro"
    sinalizacao = "sinalizacao"
    outros = "outros"


class Status(enum.Enum):
    resolvido = "resolvido"
    nao_resolvido = "nao_resolvido"


@dataclass
class Reclamacao(Base):
    __tablename__: str = "reclamacao"

    id: int = Column(BigInteger, primary_key=True)
    criacao: str = Column(DateTime, default=func.now(), nullable=False)
    modificacao: str = Column(DateTime, default=func.now(), nullable=False)
    delete: bool = Column(Boolean, default=False, nullable=False)

    descricao: str = Column(String(500), nullable=False)
    categoria: str = Column(Enum(Categoria), nullable=False)
    data: str = Column(DateTime, nullable=False)
    cep: str = Column(String(20), nullable=True)
    endereco: str = Column(String(200), nullable=False)
    numero_endereco: str = Column(String(200), nullable=False)
    ponto_referencia: str = Column(String(200), nullable=True)
    bairro: str = Column(String(200), nullable=False)
    cidade: str = Column(String(200), nullable=False)
    estado: str = Column(Enum(Estado), nullable=False)
    latitude: str = Column(String(200), nullable=False)
    longitude: str = Column(String(200), nullable=False)
    fotos: str = Column(String(2000), nullable=False)
    qtd_curtidas: int = Column(BigInteger, default=0, nullable=False)
    status: str = Column(Enum(Status), nullable=False, default="nao_resolvido")
    atualizacao_status: str = Column(DateTime, nullable=True)
    geog: str = Column(Geography(geometry_type="POINT", srid=4326), nullable=False)

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))

    def __init__(
        self,
        descricao: str,
        categoria: str,
        data: str,
        cep: str,
        endereco: str,
        numero_endereco: str,
        ponto_referencia: str,
        bairro: str,
        cidade: str,
        estado: str,
        latitude: str,
        longitude: str,
        fotos: str,
        qtd_curtidas: int,
        usuario_id: int,
        status: str,
        atualizacao_status: str,
        geog: str,
    ) -> None:
        self.descricao = descricao
        self.categoria = categoria
        self.data = data
        self.cep = cep
        self.endereco = endereco
        self.numero_endereco = numero_endereco
        self.ponto_referencia = ponto_referencia
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.latitude = latitude
        self.longitude = longitude
        self.fotos = fotos
        self.qtd_curtidas = qtd_curtidas
        self.usuario_id = usuario_id
        self.status = status
        self.atualizacao_status = atualizacao_status
        self.geog = geog


@dataclass
class Curtida(Base):
    __tablename__: str = "curtida"
    __table_args__ = (
        UniqueConstraint("usuario_id", "reclamacao_id", name="_usuario_reclamacao_uc"),
    )

    id: int = Column(BigInteger, primary_key=True)
    criacao: str = Column(DateTime, default=func.now(), nullable=False)
    modificacao: str = Column(DateTime, default=func.now(), nullable=False)
    delete: bool = Column(Boolean, default=False, nullable=False)

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    reclamacao_id: Mapped[int] = mapped_column(ForeignKey("reclamacao.id"))

    def __init__(self, usuario_id: int, reclamacao_id: int) -> None:
        self.usuario_id = usuario_id
        self.reclamacao_id = reclamacao_id


@dataclass
class Comentario(Base):
    __tablename__: str = "comentario"

    id: int = Column(BigInteger, primary_key=True)
    criacao: str = Column(DateTime, default=func.now(), nullable=False)
    modificacao: str = Column(DateTime, default=func.now(), nullable=False)
    delete: bool = Column(Boolean, default=False, nullable=False)

    texto: str = Column(String(500), nullable=False)
    reclamacao_id: Mapped[int] = mapped_column(ForeignKey("reclamacao.id"))
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))

    def __init__(self, texto: str, reclamacao_id: int, usuario_id: int) -> None:
        self.texto = texto
        self.reclamacao_id = reclamacao_id
        self.usuario_id = usuario_id
