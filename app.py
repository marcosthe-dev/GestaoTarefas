from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, text
from models import SessionLocal, ConsultaSQL
from datetime import datetime
import json


# FastAPI app
api = FastAPI(title="Gerenciador de Consultas SQL")

# Flask app
flask_app = Flask(__name__)

# Dependency para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas da API (FastAPI)
@api.get("/api/consultas")
def listar_consultas(db: Session = Depends(get_db)):
    return db.query(ConsultaSQL).all()

@api.post("/api/consultas")
def criar_consulta(titulo: str, descricao: str, query_sql: str, parametros: str, db: Session = Depends(get_db)):
    try:
        # Validar se os parâmetros são JSON válido
        if parametros:
            json.loads(parametros)
        
        consulta = ConsultaSQL(
            titulo=titulo,
            descricao=descricao,
            query_sql=query_sql,
            parametros=parametros
        )
        db.add(consulta)
        db.commit()
        db.refresh(consulta)
        return consulta
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Formato de parâmetros inválido")

@api.put("/api/consultas/{consulta_id}/desativar")
def desativar_consulta(consulta_id: int, db: Session = Depends(get_db)):
    consulta = db.query(ConsultaSQL).filter(ConsultaSQL.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    consulta.ativa = False
    db.commit()
    return consulta

# Rotas do Flask (Interface Web)
@flask_app.route("/")
def index():
    db = SessionLocal()
    consultas = db.query(ConsultaSQL).all()

    for consulta in consultas:
        try:
            conexao_dict = json.loads(consulta.conexao)
            if "password" in conexao_dict:
                conexao_dict["password"] = "********"
            consulta.conexao_mascarada = json.dumps(conexao_dict, indent=4)
        except (TypeError, json.JSONDecodeError):
            consulta.conexao_mascarada = "Erro ao interpretar conexão"

    db.close()
    return render_template("index.html", consultas=consultas)

@flask_app.route("/adicionar", methods=["POST"])
def adicionar():
    titulo = request.form.get("titulo")
    descricao = request.form.get("descricao")
    query_sql = request.form.get("query_sql")
    parametros = request.form.get("parametros")
    conexao = request.form.get("conexao")
    
    try:
        # Validar JSON dos parâmetros de conexão
        json.loads(conexao)
        if parametros:
            json.loads(parametros)
            
        db = SessionLocal()
        consulta = ConsultaSQL(
            titulo=titulo,
            descricao=descricao,
            query_sql=query_sql,
            parametros=parametros,
            conexao=conexao
        )
        db.add(consulta)
        db.commit()
        db.close()
        return redirect(url_for("index"))
    except json.JSONDecodeError:
        return "Erro: JSON inválido nos parâmetros", 400

@api.post("/api/executar/{consulta_id}")
def executar_consulta(consulta_id: int, parametros: dict, db: Session = Depends(get_db)):
    consulta = db.query(ConsultaSQL).filter(ConsultaSQL.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    if not consulta.ativa:
        raise HTTPException(status_code=400, detail="Esta consulta está inativa")
    
    try:
        # Obter parâmetros de conexão
        conexao = json.loads(consulta.conexao)
        
        # Criar conexão com o banco de dados alvo
        engine_alvo = create_engine(
            f"postgresql://{conexao['user']}:{conexao['password']}@{conexao['host']}:{conexao['port']}/{conexao['database']}"
        )
        
        # Criar sessão para o banco alvo
        SessionAlvo = sessionmaker(bind=engine_alvo)
        db_alvo = SessionAlvo()
        
        try:
            # Validar parâmetros da consulta
            if consulta.parametros:
                params_schema = json.loads(consulta.parametros)
                for param, tipo in params_schema.items():
                    if param not in parametros:
                        raise HTTPException(
                            status_code=400, 
                            detail=f"Parâmetro obrigatório ausente: {param}"
                        )
                    
                    # Converter tipos de dados
                    if tipo.lower() == 'integer':
                        parametros[param] = int(parametros[param])
                    elif tipo.lower() in ['decimal', 'float']:
                        parametros[param] = float(parametros[param])
            
            # Executar a consulta no banco alvo
            result = db_alvo.execute(text(consulta.query_sql), parametros)
            
            # Converter resultado para lista de dicionários
            columns = result.keys()
            return [dict(zip(columns, row)) for row in result.fetchall()]
            
        finally:
            db_alvo.close()
            engine_alvo.dispose()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar consulta: {str(e)}")

# Nova rota para a interface de execução de consultas
@flask_app.route("/executar")
def executar():
    db = SessionLocal()
    consultas = db.query(ConsultaSQL).all()
    db.close()
    return render_template("executar_consulta.html", consultas=consultas)

# Nova rota da API para executar consultas
@api.post("/api/executar/{consulta_id}")
def executar_consulta(consulta_id: int, parametros: dict, db: Session = Depends(get_db)):
    consulta = db.query(ConsultaSQL).filter(ConsultaSQL.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    
    if not consulta.ativa:
        raise HTTPException(status_code=400, detail="Esta consulta está inativa")
    
    try:
        # Validar parâmetros
        params_schema = json.loads(consulta.parametros)
        for param, tipo in params_schema.items():
            if param not in parametros:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Parâmetro obrigatório ausente: {param}"
                )
            
            # Converter tipos de dados
            if tipo.lower() == 'integer':
                parametros[param] = int(parametros[param])
            elif tipo.lower() in ['decimal', 'float']:
                parametros[param] = float(parametros[param])
            # Para datas e strings, mantemos como estão
        
        # Executar a consulta
        result = db.execute(text(consulta.query_sql), parametros)
        
        # Converter resultado para lista de dicionários
        columns = result.keys()
        return [dict(zip(columns, row)) for row in result.fetchall()]
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro de validação: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar consulta: {str(e)}")

# Montando o Flask app no FastAPI
api.mount("/", WSGIMiddleware(flask_app))