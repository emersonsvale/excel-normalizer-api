from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import re
from typing import List, Dict, Any
import io
import logging
import traceback

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        # Log das colunas originais
        logger.info(f"Colunas originais: {df.columns.tolist()}")
        
        # Normaliza os nomes das colunas
        df.columns = [normalize_column_name(col) for col in df.columns]
        logger.info(f"Colunas normalizadas: {df.columns.tolist()}")
        
        # Verifica se a coluna 'location' existe
        if 'location' not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"Coluna 'Location' não encontrada no arquivo Excel. Colunas disponíveis: {df.columns.tolist()}"
            )
        
        # Filtra registros sem location
        df = df.dropna(subset=['location'])
        logger.info(f"Número de registros após filtrar location nulos: {len(df)}")
        
        # Converte o DataFrame para lista de dicionários
        result = df.to_dict(orient='records')
        logger.info(f"Número de registros convertidos: {len(result)}")
        
        return result
    
    except Exception as e:
        logger.error(f"Erro ao processar dados: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados: {str(e)}")

@app.post("/upload")
async def upload_excel(file: UploadFile):
    """
    Endpoint para upload de arquivo Excel.
    
    Args:
        file (UploadFile): Arquivo Excel (.xlsx)
        
    Returns:
        JSONResponse: Dados da planilha em formato JSON
    """
    try:
        logger.info(f"Recebendo arquivo: {file.filename}")
        
        if not file.filename.endswith('.xlsx'):
            raise HTTPException(status_code=400, detail="Apenas arquivos .xlsx são aceitos")
        
        # Lê o conteúdo do arquivo
        contents = await file.read()
        logger.info(f"Tamanho do arquivo: {len(contents)} bytes")
        
        # Converte para DataFrame
        df = pd.read_excel(io.BytesIO(contents))
        logger.info(f"DataFrame criado com {len(df)} linhas e {len(df.columns)} colunas")
        
        # Processa os dados
        result = process_excel_data(df)
        
        return JSONResponse(content=result)
    
    except HTTPException as he:
        logger.error(f"Erro HTTP: {str(he)}")
        raise he
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        logger.error(traceback.format_exc())
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