from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pytz import timezone
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class ConsultaSQL(Base):
    __tablename__ = "consultas_sql"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String)
    query_sql = Column(Text, nullable=False)
    parametros = Column(String)
    conexao = Column(String, nullable=False)
    tipo_banco = Column(String, nullable=False)  # mysql, postgresql, oracle
    ativa = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.now(timezone('America/Sao_Paulo')))

Base.metadata.create_all(bind=engine)