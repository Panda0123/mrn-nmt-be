# Maranao-English Translation API

A FastAPI-based RESTful API for translating between Maranao and English languages using T5 transformer models.

## Features

- Bidirectional translation between Maranao and English
- RESTful API with JSON request/response
- Automatic documentation with Swagger UI
- Error handling and validation

## Requirements

- Python 3.12.9
- FastAPI
- Uvicorn
- Transformers
- PyTorch
- python-dotenv
- Finetuned T5 model for Maranao-English translation

## Installation

1. Clone this repository
2. Install dependencies using uv:
   ```
   uv pip install -r requirements.txt
   ```
   
   Or using pip:
   ```
   pip install -r requirements.txt
   ```
3. Download and set up the model:
   - Download the finetuned [model](https://drive.google.com/file/d/1ZQcOaMBqrAbUMwvwqawJ53ndKInXlVlX/view)
   - Unzip the downloaded file
   - Place the extracted model files in the `./models` directory
4. Set up authentication:
   - Create a `.env` file based on the `.env.example`
   - Add your secret API key: `API_KEY=your_secure_api_key_here`

## Running the API

Start the server with:

```
python app.py
```

Or:

```
uvicorn app:app --reload
```

The server will start at http://0.0.0.0:8000 by default.

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

All translation requests require authentication using an API key.

- Add the API key to the request headers as `X-API-Key`
- The API key must match the one specified in your `.env` file

## API Endpoints

### POST /translate

Translates text between Maranao and English.

#### Request Headers

```
X-API-Key: your_api_key_here
```

#### Request Body

```json
{
  "source_lang": "MARANAO",  // or "ENGLISH"
  "target_lang": "ENGLISH",  // or "MARANAO"
  "source_text": "Anda ka song?"
}
```

#### Response

```json
{
  "source_lang": "MARANAO",
  "target_lang": "ENGLISH",
  "source_text": "Anda ka song?",
  "target_text": "Where are you going?"
}
```

## Example Usage

### cURL

```bash
curl -X 'POST' \
  'http://localhost:8000/translate' \
  -H 'Content-Type: application/json' \
  -H 'X-API-Key: your_api_key_here' \
  -d '{
  "source_lang": "MARANAO",
  "target_lang": "ENGLISH",
  "source_text": "Anda ka song?"
}'
```

### Python

```python
import requests

url = "http://localhost:8000/translate"
headers = {
    "X-API-Key": "your_api_key_here"
}
payload = {
    "source_lang": "MARANAO",
    "target_lang": "ENGLISH",
    "source_text": "Anda ka song?"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

## Error Handling

The API returns appropriate HTTP status codes:

- 400: Bad Request (invalid parameters)
- 401: Unauthorized (missing API key)
- 403: Forbidden (invalid API key)
- 500: Server Error (translation failure)

Each error response includes a detail message explaining the issue.

## TODOs

- Add support for batch translation
- Implement rate limiting
- Add translation memory for frequently translated phrases