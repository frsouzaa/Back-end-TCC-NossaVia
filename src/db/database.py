from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, func, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()
engine = create_engine(os.getenv("DB_URI"))
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
metadata = Base.metadata


@dataclass
class Usuario(Base):
    __tablename__ = "usuario"

    id: int = Column(Integer, primary_key=True)
    nome: str = Column(String(200), nullable=False)
    email: str = Column(String(200), unique=True, nullable=False)
    senha: str = Column(String(200), nullable=False)
    endereco: str = Column(String(200), nullable=False)
    cep: str = Column(String(20), nullable=False)
    nascimento: str = Column(DateTime, nullable=False)
    pontucao: int = Column(Integer, nullable=False)
    create_at: str = Column(DateTime, default=func.now(), nullable=False)

    def __init__(self, nome, email, senha, endereco, cep, nascimento, pontucao):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.senha = senha
        self.endereco = endereco
        self.cep = cep
        self.nascimento = nascimento
        self.pontucao = pontucao
