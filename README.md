# FastAPI Project

Este projeto é um exemplo de aplicação FastAPI que utiliza o `llama-index` para consulta de documentos e retorna a resposta em formato Markdown.

## Visão Geral

A aplicação é configurada para ingerir documentos e realizar consultas nos documentos usando o `llama-index`. Foi pensado apenas para uso pessoal. Sem otimizações, focando apenas nos prompts para uma boa resposta em PDFs científico.

## Instalação

### Pré-requisitos

- Python 3.12.3
- Virtualenv

### Passos

1. Clone o repositório:

```bash
git clone https://github.com/usuario/fastapi_project.git
cd fastapi_project
```

2.	Crie e ative um ambiente virtual:

```bash
python -m venv env
source env/bin/activate  # No Windows use `env\Scripts\activate`
```

3. Instale as dependências:

```bash
pip install .
```

4. Crie um arquivo .env na raiz do projeto com as seguintes variáveis de ambiente:

```
OPENAI_API_KEY=**** [gerado no site da openai]
PDFS_FOLDER=pdfs
PERSIST_DIRECTORY=persist_dir
MODEL=gpt-3.5-turbo
TEMPERATURE=0
MAX_TOKENS=1000
EMBED_MODEL=text-embedding-3-small
```

### Configuração

Configure as variáveis de ambiente no arquivo .env conforme suas necessidades. As variáveis disponíveis são:

*  PDFS_FOLDER: Diretório com os pdfs a serem indexados
*  PERSIST_DIRECTORY: Diretório para persistência dos dados
*  MODEL: Modelo a ser utilizado pelo OpenAI
*  EMPERATURE: Temperatura para o modelo OpenAI
*  TOKENS: Número máximo de tokens para a resposta do modelo
*  EMBED_MODEL: Modelo de embedding a ser utilizado

# Execução

1.	Inicie o servidor FastAPI:

 ```bash
uvicorn app.main:app --reload
```

2.	Acesse a documentação interativa (Swagger UI) em http://127.0.0.1:8000/docs.

# Endpoints

Ingestão de Documentos

	•	URL: /ingestion
	•	Método: POST
	•	Descrição: Ingesta documentos no sistema.
	•	Resposta:
	•	200 OK: Documentos ingeridos com sucesso.
	•	500 Internal Server Error: Erro na ingesta dos documentos.

Consulta de Documentos

	•	URL: /query
	•	Método: POST
	•	Descrição: Realiza uma consulta aos documentos ingeridos e retorna a resposta em formato Markdown.
	•	Request Body:
	•	question: Pergunta a ser feita ao sistema.
	•	Resposta:
	•	200 OK: Resposta à pergunta em formato Markdown renderizado.
	•	500 Internal Server Error: Erro ao realizar a consulta.

Exemplo de Requisição de Consulta

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "O que é FastAPI?"
}'
```
