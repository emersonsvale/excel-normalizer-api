# Excel to JSON Converter API

API em FastAPI para converter arquivos Excel (.xlsx) em formato JSON.

## Features

* Upload de arquivos Excel via endpoint POST
* Normalização dos nomes das colunas (minúsculas, remoção de espaços)
* Retorno dos dados em formato JSON
* Suporte a Docker
* Deploy na Vercel

## Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/emersonsvale/excel-normalizer-api.git
cd excel-normalizer-api
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando a Aplicação

Para iniciar o servidor:

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Endpoints

### POST /upload
Endpoint para upload de arquivo Excel.

**Requisitos do arquivo Excel:**
- Formato: .xlsx
- Colunas esperadas:
  - Region: Região geográfica
  - Country: País
  - Number: Identificador numérico
  - Location: Coordenadas no formato WKT (POINT Z)

**Exemplo de uso com curl:**
```bash
curl -X POST "http://localhost:8000/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@seu_arquivo.xlsx"
```

### GET /
Endpoint raiz com informações sobre a API.

## Docker Support

Para construir e executar o container Docker:

```bash
docker build -t excel-normalizer .
docker run -p 8000:8000 excel-normalizer
```

## Deploy

Esta aplicação pode ser deployada na Vercel usando a configuração `vercel.json` fornecida.

## Documentação da API

A documentação interativa da API está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Licença

MIT
