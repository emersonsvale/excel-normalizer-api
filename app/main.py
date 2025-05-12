from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import io
import logging
from .utils import process_excel

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Excel Normalizer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Excel Normalizer API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Log que recebemos o arquivo
    logger.info(f"Recebido arquivo: {file.filename}")
    
    # Validate file extension
    if not file.filename.endswith(('.xlsx', '.xls')):
        logger.warning(f"Formato de arquivo não suportado: {file.filename}")
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are supported")
    
    try:
        # Read the file content
        logger.info("Lendo conteúdo do arquivo")
        content = await file.read()
        logger.info(f"Arquivo lido com sucesso: {len(content)} bytes")
        
        # Process the Excel file
        logger.info("Processando arquivo Excel")
        excel_data = process_excel(io.BytesIO(content))
        logger.info(f"Processamento concluído: {len(excel_data)} registros encontrados")
        
        # Return the processed data
        return {"filename": file.filename, "data": excel_data}
    
    except Exception as e:
        # Log the detailed error
        error_msg = str(e)
        logger.error(f"Erro ao processar arquivo: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {error_msg}")

# Special handler for Vercel serverless
@app.get("/api/health")
async def health():
    return {"status": "ok"} 