from fastapi import FastAPI, HTTPException, Security, Depends, Header
from pydantic import BaseModel
from transformers import T5ForConditionalGeneration, T5Tokenizer
from typing import Literal, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY", "default_key_for_development")

# Initialize the FastAPI app
app = FastAPI(
    title="Maranao-English Translation API",
    description="API for translating between Maranao and English languages",
    version="1.0.0"
)

# Define the request and response models
class TranslationRequest(BaseModel):
    source_lang: Literal["MARANAO", "ENGLISH"]
    target_lang: Literal["MARANAO", "ENGLISH"]
    source_text: str

class TranslationResponse(TranslationRequest):
    target_text: str

# Authentication dependency
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key is missing. Please provide 'X-API-Key' header.",
            headers={"WWW-Authenticate": "API-Key"},
        )
    
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "API-Key"},
        )
    
    return x_api_key

# Load the models (this happens only once when the server starts)
try:
    small_model = T5ForConditionalGeneration.from_pretrained("./models/MRN_NMT_T5_small", from_tf=False)
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    print("Models loaded successfully")
except Exception as e:
    print(f"Error loading models: {str(e)}")
    raise

# Helper function
def translate(model, tokenizer, src: str):
    tok = tokenizer(src, return_tensors="pt").input_ids
    res = model.generate(tok)
    decoded = tokenizer.decode(res[0])
    return decoded[6:-4]  # remove sos and eos

@app.post("/translate", response_model=TranslationResponse)
async def translate_text(
    request: TranslationRequest,
    api_key: str = Depends(verify_api_key)
):
    # Validate that source and target languages are different
    if request.source_lang == request.target_lang:
        raise HTTPException(
            status_code=400, 
            detail="Source and target languages must be different"
        )
        
    # Determine the direction of translation
    if request.source_lang == "MARANAO" and request.target_lang == "ENGLISH":
        # Maranao to English
        prefix = "translate Maranao to English: "
        src = prefix + request.source_text
    elif request.source_lang == "ENGLISH" and request.target_lang == "MARANAO":
        # English to Maranao
        prefix = "translate English to Maranao: "
        src = prefix + request.source_text
    else:
        raise HTTPException(
            status_code=400, 
            detail="Invalid language combination. Supported: MARANAO to ENGLISH or ENGLISH to MARANAO."
        )
    
    try:
        # Perform the translation
        translated_text = translate(small_model, tokenizer, src)
        
        # Return the response
        return TranslationResponse(
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            source_text=request.source_text,
            target_text=translated_text
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Translation error: {str(e)}"
        )

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Maranao-English Translation API",
        "usage": "POST to /translate with JSON body containing source_lang, target_lang, and source_text",
        "authentication": "API Key required in X-API-Key header"
    }

# Run the server directly if this file is executed
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 