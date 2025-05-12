from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import re
from typing import List, Dict, Any
import io

app = FastAPI(
    title="Excel to JSON Converter",
    description="API para converter arquivos Excel em formato JSON",
    version="1.0.0"
)

def normalize_column_name(column: str) -> str:
    """Normaliza o nome da coluna removendo espaços e convertendo para minúsculas."""
    return re.sub(r'\s+', '', column.lower())

def process_excel_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Processa os dados do DataFrame e retorna uma lista de dicionários."""
    # Normaliza os nomes das colunas
    df.columns = [normalize_column_name(col) for col in df.columns]
    
    # Verifica se a coluna 'location' existe
    if 'location' not in df.columns:
        raise HTTPException(status_code=400, detail="Coluna 'Location' não encontrada no arquivo Excel")
    
    # Filtra registros sem location
    df = df.dropna(subset=['location'])
    
    # Converte o DataFrame para lista de dicionários
    result = df.to_dict(orient='records')
    
    return result

@app.post("/upload")
async def upload_excel(file: UploadFile):
    """
    Endpoint para upload de arquivo Excel.
    
    Args:
        file (UploadFile): Arquivo Excel (.xlsx)
        
    Returns:
        JSONResponse: Dados da planilha em formato JSON
    """
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="Apenas arquivos .xlsx são aceitos")
    
    try:
        # Lê o conteúdo do arquivo
        contents = await file.read()
        
        # Converte para DataFrame
        df = pd.read_excel(io.BytesIO(contents))
        
        # Processa os dados
        result = process_excel_data(df)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")

@app.get("/")
async def root():
    """Endpoint raiz com informações sobre a API."""
    return {
        "message": "Bem-vindo à API de conversão Excel para JSON",
        "endpoints": {
            "/upload": "POST - Envie um arquivo Excel para converter em JSON"
        }
    } 