from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import io
from .utils import process_excel

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
    # Validate file extension
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only Excel files (.xlsx, .xls) are supported")
    
    try:
        # Read the file content
        content = await file.read()
        
        # Process the Excel file
        excel_data = process_excel(io.BytesIO(content))
        
        # Return the processed data
        return {"filename": file.filename, "data": excel_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}") 