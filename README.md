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
git clone https://github.com/marcosthe-dev/GestaoTarefas.git
cd GestaoTarefas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configuração do Banco de Dados
    ## Configuração do Banco de Dados PostgreSQL

    ### Pré-requisitos
    - PostgreSQL 12 ou superior instalado
    - Acesso de administrador ao PostgreSQL

    ### Criando o Banco de Dados de Teste

    1. Acesse o PostgreSQL via psql ou pgAdmin

    2. Execute os seguintes comandos SQL:

    ```sql
    -- Criar banco de dados
    CREATE DATABASE gestao_tarefas;

    -- Conectar ao banco criado
    \c gestao_tarefas

    -- Criar tabela de consultas
    CREATE TABLE consultas_sql (
        id SERIAL PRIMARY KEY,
        titulo VARCHAR(255) NOT NULL,
        descricao TEXT,
        query_sql TEXT NOT NULL,
        parametros TEXT,
        conexao TEXT NOT NULL,
        tipo_banco VARCHAR(50) NOT NULL,
        ativa BOOLEAN DEFAULT TRUE,
        data_criacao TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    ```	
    ### Dados de Exemplo
    Execute os seguintes comandos para inserir algumas consultas de teste:

    ```sql
    INSERT INTO consultas_sql (
    titulo, 
    descricao, 
    query_sql, 
    parametros, 
    conexao, 
    tipo_banco
    ) VALUES (
        'Consulta de Clientes por Data',
        'Lista todos os clientes cadastrados após uma data específica',
        'SELECT * FROM clientes WHERE data_cadastro >= :data_inicio',
        '{"data_inicio": "date"}',
        '{"host": "localhost", "port": 5432, "database": "seu_banco", "user": "seu_usuario", "password": "sua_senha"}',
        'postgresql'
    );

    INSERT INTO consultas_sql (
        titulo, 
        descricao, 
        query_sql, 
        parametros, 
        conexao, 
        tipo_banco
    ) VALUES (
        'Total de Vendas por Período',
        'Calcula o total de vendas em um período específico',
        'SELECT COUNT(*) as total, SUM(valor) as valor_total FROM vendas WHERE data_venda BETWEEN :data_inicio AND :data_fim',
        '{"data_inicio": "date", "data_fim": "date"}',
        '{"host": "localhost", "port": 5432, "database": "seu_banco", "user": "seu_usuario", "password": "sua_senha"}',
        'postgresql'
    );
    ```

    ### Configuração no arquivo models.py
    Atualize a string de conexão no arquivo models.py :

    ```python
    DATABASE_URL = "postgresql://seu_usuario:sua_senha@localhost:5432/gestao_tarefas"
    ```

    Substitua "usuario" e "senha" pelos seus dados de acesso ao PostgreSQL.

    ### Verificando a Instalação
    1. Execute a aplicação:
    ```bash
    uvicorn app:api --reload
    ```
    2. Acesse http://localhost:8000 no navegador
    3. Você deverá ver as consultas de exemplo cadastradas na interface
    ### Observações de Segurança
    - Em ambiente de produção, use variáveis de ambiente para as credenciais
    - Não armazene senhas em texto plano no banco de dados
    - Limite o acesso do usuário do banco apenas às operações necessárias
    - Faça backup regular dos dados

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
