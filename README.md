# Excel Normalizer API

A FastAPI application that receives Excel files (.xlsx), normalizes column names, and returns data in JSON format.

## Features

- Upload Excel files via a POST endpoint
- Normalize column names (lowercase, remove spaces, replace special characters)
- Return data as JSON

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies:
```bash
pip install -r app/requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Usage

### API Endpoints

- `GET /`: Check if the API is running
- `POST /upload`: Upload an Excel file for processing

### Example Request

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_excel_file.xlsx"
```

### Example Response

```json
{
  "filename": "your_excel_file.xlsx",
  "data": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com"
    }
  ]
}
```

## Docker Support

Build and run the Docker container:

```bash
docker build -t excel-normalizer .
docker run -p 8000:8000 excel-normalizer
```

## Deployment

This application can be deployed to Vercel using the provided `vercel.json` configuration.

## License

MIT 