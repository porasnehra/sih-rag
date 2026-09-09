from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from query_understanding import analyze_query
from vector_store import search_vectors
from generation import detect_and_translate, generate_response

load_dotenv()

app = FastAPI(title="BIS Standards RAG API")

# Add CORS middleware to allow the Flutter frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str] = []

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    user_query = request.query
    if not user_query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        # 1. Translate if needed
        english_query, is_hindi = detect_and_translate(user_query)
        
        # 2. Retrieve Context
        results = search_vectors(english_query, k=3)
        THRESHOLD = 1.0
        valid_results = [r for r in results if r['score'] < THRESHOLD]
        if not valid_results and results:
            valid_results = []
            
        # 3. Generate Response
        final_output = generate_response(english_query, valid_results, is_hindi=is_hindi)
        
        # 4. Return structured JSON
        if isinstance(final_output, dict):
            return QueryResponse(
                answer=final_output.get("answer", "No answer generated."),
                sources=final_output.get("sources", [])
            )
        else:
            return QueryResponse(answer=str(final_output), sources=[])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "BIS RAG API is running"}
