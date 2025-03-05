# API RAG com Python

Este é um projeto de API baseada em FastAPI que implementa Retrieval-Augmented Generation (RAG) para responder perguntas com base no conteúdo de "Origin of Species" de Charles Darwin. A API utiliza embeddings, um banco vetorial (Chroma) e um modelo de linguagem (Ollama, rodando o llama3.2:3b localmente) para processar consultas.


## Requisitos

- Python 3.10 ou superior
- Ollama (instalado localmente para o modelo de linguagem)
- Dependências Python listadas em `requirements.txt`

## Instalação

### 1. Clonar o Repositório
```bash
    git clone https://github.com/FabbSantos/api-rag-py.git
    cd api-rag-py
```

### 2. Instalar Dependências
#### 2.1 - Crie um ambiente virtual e instale as bibliotecas:

```bash
    python3.10 -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install -r requirements.txt
```
### 3. Instalar e Configurar Ollama

##### 3.1 - Baixe e instale o Ollama em https://ollama.com/

##### 3.2 - Inicie o servidor Ollama:

```bash
    ollama serve
```
#### 3.3 - Baixe o modelo especificado:

```bash
    ollama run llama3.2:3b
```
#### 3.4 - Quando estiver pronto, saia com /bye e deixe o servidor rodando.

### OPT.: Se quiser alterar algum modelo, edite o arquivo 
<code>app/utils/config.yaml</code>

### 4. Certifique-se de que o arquivo data/origin_of_species.md está no diretório data/.

#### 4.1 - A indexação do documento ocorre automaticamente ao iniciar a API.


## Execução

### 1. Inicie a API:
```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 2. Acesse a API em http://localhost:8000/docs para visualizar a documentação da API.

### 3. Utilize algum API Client (Postman, Insomnia, Thunder Client, etc) para enviar um POST para http://localhost:8000/query com o seguinte JSON:
```json
    {
        "query": "what is the book about?"
    }
```
#### 3.1 - A resposta será algo como:
```json
    {
    "response": "The book explores the theory of evolution by natural selection...",
    "sources": ["data/origin_of_species.md"]
    }
```

## Estratégia do RAG

####  Pré processei o arquivo origin_of_species para markdown e o carreguei em um banco de dados Chroma.

####  Usei um modelo de embeddings (sentence-transformers/all-MiniLM-L6-v2) pra criar um banco vetorial com Chroma, recuperando os k=5 chunks mais relevantes por similaridade de cosseno. (Retrieval)

#### Combinei os documentos recuperados com a query no modelo Ollama (llama3.2:3b) para gerar uma resposta. (Augmentation)

#### A aplicação gera respostas com base no contexto, usando um prompt otimizado.

## Estratégias para evolução do produto:

#### 1. Adicionar a possibilidade de usar outras fontes de dados para o RAG.
#### 2. Usar modelos melhores tanto para embeddings quanto para o modelo de linguagem, como o llama3.2-vision, que permite a entrada de imagens.
#### 3. Fazer o  deploy da API em um ambiente de produção (GCP, AWS, Azure, Oracle) quando tiver recursos para isso.
#### 4. Adicionar um histórico de mensagens eficiente para a conversação com o usuário.
#### 5. Implementar um sistema de cache com Redis para acelerar as consultas.
#### 6. Adicionar um sistema de feedback, utilizando análise de sentimento, e treinamento para melhorar a precisão das respostas.



