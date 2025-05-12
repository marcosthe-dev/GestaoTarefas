# Gerenciador de Consultas SQL

Este projeto consiste em um sistema web para cadastro, execução e gerenciamento de consultas SQL parametrizadas, com suporte a múltiplos bancos de dados relacionais. A aplicação oferece uma interface intuitiva, exportação de resultados e mecanismos de segurança para ambientes corporativos.

## ✅ Funcionalidades

- Cadastro de consultas SQL com parâmetros definidos em JSON
- Suporte a múltiplos bancos de dados: PostgreSQL, MySQL e Oracle
- Interface web para execução de consultas de forma simplificada
- Exportação de resultados em formatos CSV e Excel
- Gerenciamento de conexões com diferentes bancos de dados
- Validação dos tipos de dados dos parâmetros de entrada
- Ativação e desativação de consultas pelo administrador

## 🛠️ Requisitos

- Python 3.7 ou superior  
- Bibliotecas:
  - FastAPI
  - Flask
  - SQLAlchemy
  - psycopg2 (PostgreSQL)
  - PyMySQL (MySQL)
  - oracledb (Oracle)

## 🚀 Instalação

### 1. Clonagem do Repositório

```bash
git clone https://github.com/marcosthe-dev/GestaoTarefas.git
cd GestaoTarefas
```

### 2. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados a Ser Consultado Pelo Cliente.

Para testar a aplicação, é necessário criar um banco de dados e inserir dados de exemplo para simular uma consulta SQL. Siga as instruções abaixo para criar as tabelas e inserir dados de exemplo.

#### Pré-requisitos

- PostgreSQL 12 ou superior
- Permissões de administrador no PostgreSQL

#### Criação das Tabelas de Teste

Acesse o PostgreSQL via `psql` ou `pgAdmin` e execute os seguintes comandos para criar as tabelas de teste:

```sql
CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    categoria VARCHAR(50)
);

CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    produto_id INT REFERENCES produtos(id),
    valor NUMERIC(10,2),
    data_venda DATE
);
```

#### Inserção de Dados de Exemplo

```sql
-- Inserção de Produtos
INSERT INTO produtos (nome, categoria) VALUES 
('Notebook Dell', 'Informática'),
('Mouse Logitech', 'Informática'),
('Cadeira Gamer', 'Móveis'),
('Mesa Escritório', 'Móveis'),
('Fone Bluetooth', 'Eletrônicos'),
('Smartphone Xiaomi', 'Eletrônicos');

-- Inserção de Vendas
INSERT INTO vendas (produto_id, valor, data_venda) VALUES
(1, 3500.00, '2025-05-01'),
(1, 3600.00, '2025-05-03'),
(2, 150.00,  '2025-05-02'),
(2, 155.00,  '2025-05-04'),
(3, 900.00,  '2025-05-01'),
(4, 1200.00, '2025-05-02'),
(4, 1250.00, '2025-05-03'),
(5, 200.00,  '2025-05-02'),
(5, 210.00,  '2025-05-05'),
(6, 1800.00, '2025-05-03'),
(6, 1900.00, '2025-05-04');
```

#### Exemplo de Consulta SQL com Parâmetros

```sql
SELECT 
    p.categoria,
    COUNT(v.id) AS total_vendas,
    SUM(v.valor) AS valor_total,
    AVG(v.valor) AS ticket_medio
FROM vendas v
JOIN produtos p ON v.produto_id = p.id
WHERE 
    v.data_venda BETWEEN '2025-05-01' AND '2025-05-05'
    AND ('Eletrônicos' IS NULL OR p.categoria = 'Eletrônicos')
GROUP BY p.categoria
ORDER BY valor_total DESC;
```

#### Configuração do Banco de Dados a Ser Gerenciado Pelo Administrador

Para gerenciar as consultas SQL, é necessário criar uma tabela no banco de dados de gestão das consultas. Siga as instruções abaixo para criar a tabela e inserir dados de exemplo.

```sql
CREATE DATABASE gestao_tarefas;

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

#### Inserção de Dados de Exemplo de Consultas

```sql
INSERT INTO consultas_sql (
    titulo, descricao, query_sql, parametros, conexao, tipo_banco
) VALUES (
    'Total de Vendas por Período',
    'Calcula o total de vendas em um período específico',
    'SELECT COUNT(*) as total, SUM(valor) as valor_total FROM vendas WHERE data_venda BETWEEN :data_inicio AND :data_fim',
    '{"data_inicio": "date", "data_fim": "date"}',
    '{"host": "localhost", "port": 5432, "database": "seu_banco", "user": "seu_usuario", "password": "sua_senha"}',
    'postgresql'
);
```

#### Configuração da String de Conexão

No arquivo `models.py`, configure a variável `DATABASE_URL` com suas credenciais:

```python
DATABASE_URL = "postgresql://seu_usuario:sua_senha@localhost:5432/gestao_tarefas"
```

> Substitua `seu_usuario` e `sua_senha` pelas suas credenciais reais.

### 4. Execução da Aplicação

```bash
uvicorn app:api --reload
```

Acesse a aplicação em: [http://localhost:8000](http://localhost:8000)

## 📁 Estrutura do Projeto

```
GestaoTarefas/
├── app.py                   # Arquivo principal (integração FastAPI + Flask)
├── models.py                # Modelos e configurações de banco de dados
├── requirements.txt         # Lista de dependências do projeto
└── templates/               # Templates HTML para a interface web
    ├── index.html
    └── executar_consulta.html
```

## 🧩 Uso

### Cadastro de Consultas

1. Acesse a página inicial.
2. Preencha os campos obrigatórios:
   - **Título**
   - **Descrição**
   - **Consulta SQL**
   - **Parâmetros (em formato JSON)**
   - **Configuração da conexão (em formato JSON)**

### Execução de Consultas

1. Acesse a página de execução.
2. Selecione a consulta desejada.
3. Informe os parâmetros exigidos.
4. Clique em "Executar".
5. Se necessário, exporte os resultados para CSV ou Excel.

## 🧾 Exemplos de Parâmetros

### Parâmetros da Consulta (JSON)

```json
{
  "data_inicio": "date",
  "id_cliente": "integer",
  "nome": "string"
}
```

### Configuração de Conexão (JSON)

```json
{
  "host": "localhost",
  "port": 5432,
  "database": "nome_banco",
  "user": "usuario",
  "password": "senha"
}
```

## 🔐 Segurança

- Senhas são mascaradas na interface de configuração
- Validação de JSON para parâmetros e conexões
- Controle de ativação/desativação de consultas
- Tratamento de exceções em conexões com bancos
- Recomendações:
  - Utilize variáveis de ambiente para armazenar credenciais
  - Nunca armazene senhas em texto plano
  - Conceda permissões mínimas ao usuário de banco
  - Realize backups periódicos dos dados

## 🤝 Contribuindo

1. Faça um *fork* deste repositório
2. Crie uma nova *branch* com sua funcionalidade
3. Realize os *commits*
4. Envie um *pull request*

## 📄 Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).

---

Desenvolvido com ❤️ para facilitar o gerenciamento de consultas SQL em ambientes corporativos.