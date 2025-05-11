# Gerenciador de Consultas SQL

Este é um sistema de gerenciamento de consultas SQL que permite criar, executar e gerenciar consultas em diferentes bancos de dados (PostgreSQL, MySQL e Oracle).

## Funcionalidades

- Cadastro de consultas SQL com parâmetros
- Suporte a múltiplos bancos de dados (PostgreSQL, MySQL, Oracle)
- Interface web amigável para execução de consultas
- Exportação de resultados em CSV e Excel
- Gerenciamento de parâmetros de conexão
- Validação de tipos de dados dos parâmetros
- Sistema de ativação/desativação de consultas

## Requisitos

- Python 3.7+
- FastAPI
- Flask
- SQLAlchemy
- Psycopg2 (PostgreSQL)
- PyMySQL (MySQL)
- OracleDB (Oracle)

## Instalação

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd GestaoTarefas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o banco de dados no arquivo `models.py`

4. Execute a aplicação:
```bash
uvicorn app:api --reload
```

## Estrutura do Projeto

```
GestaoTarefas/
├── app.py              # Aplicação principal (FastAPI + Flask)
├── models.py           # Modelos do banco de dados
├── requirements.txt    # Dependências do projeto
└── templates/          # Templates HTML
    ├── index.html      # Página inicial
    └── executar_consulta.html  # Interface de execução
```

## Uso

### Cadastro de Consultas

1. Acesse a página inicial
2. Preencha os campos:
   - Título da consulta
   - Descrição
   - Query SQL
   - Parâmetros (formato JSON)
   - Configuração de conexão (formato JSON)

### Execução de Consultas

1. Acesse a página de execução
2. Selecione a consulta desejada
3. Preencha os parâmetros solicitados
4. Execute a consulta
5. Exporte os resultados em CSV ou Excel se necessário

## Formatos de Parâmetros

### Parâmetros da Consulta
```json
{
    "parametro1": "integer",
    "parametro2": "date",
    "parametro3": "string"
}
```

### Configuração de Conexão
```json
{
    "host": "localhost",
    "port": 5432,
    "database": "nome_banco",
    "user": "usuario",
    "password": "senha"
}
```

## Segurança

- Senhas são mascaradas na interface
- Validação de JSON para parâmetros
- Controle de consultas ativas/inativas
- Tratamento de erros para conexões falhas

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das alterações
4. Envie um pull request

## Licença

Este projeto está sob a licença MIT.

---

Desenvolvido com ❤️ para facilitar o gerenciamento de consultas SQL em ambientes corporativos.
