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

# --- NEW ENDPOINTS FOR FLUTTER FRONTEND ---

@app.get("/standard-details/{is_number}")
async def get_standard_details(is_number: str):
    """
    Fetches detailed structured data for a given standard.
    This provides compliance, scope & material, testing requirements, and ISI marks mandate.
    """
    # Note: Returning mocked data structured exactly as requested by the frontend
    return {
        "is_number": is_number,
        "compliance": {
            "status": True,
            "badge": "QCO ENFORCED",
            "order_type": "BIS Quality Control Order (QCO)",
            "gazette_reference": "Gazette S.O. 504(E)",
            "enforced_from": "March 2024"
        },
        "scope_and_material": {
            "material_grade_specification": {
                "title": "Material Grade Specification",
                "description": f"Standardized composition for {is_number}",
                "composition_limits": {
                    "chromium": {"operator": ">=", "value": 17.5, "unit": "%"},
                    "nickel": {"operator": ">=", "value": 8.0, "unit": "%"},
                    "carbon": {"operator": "<=", "value": 0.08, "unit": "%"}
                }
            }
        },
        "testing_requirements": {
            "section": "Clause 7",
            "total_criteria": 4,
            "criteria": [
                {
                    "id": "Q1",
                    "title": "Thermal Performance Test",
                    "description": "Measures heat retention over time",
                    "status": "mandatory",
                    "requirement": {
                        "type": "temperature_drop",
                        "operator": "<",
                        "value": 20,
                        "unit": "°C",
                        "time": "6 hours"
                    }
                }
            ]
        },
        "isi_requirements": {
            "conformity_route": "Scheme-I",
            "factory_audit": True,
            "lab_tests": True,
            "marking_type": "Standard ISI",
            "license_id": {
                "required": True,
                "format": "7-Digit CM/L License ID"
            },
            "base_plate_stamp": {
                "required": True,
                "elements": ["ISI Mark", "CM/L", "QR"],
                "application_method": "Laser etched or permanently embossed"
            }
        }
    }

@app.get("/laboratories/{is_number}")
async def get_laboratories(is_number: str):
    """
    Fetches accredited testing laboratories capable of testing the requested standard.
    Includes accreditation status, testing capabilities, turnaround times, and sample submission info.
    """
    return {
        "is_number": is_number,
        "laboratories": [
            {
                "id": "lab_001",
                "name": "National Test House (NTH)",
                "location": {
                    "city": "Mumbai",
                    "state": "Maharashtra"
                },
                "contact": {
                    "email": "contact@nth.gov.in",
                    "phone": "+91-11-23345678"
                },
                "accreditation": {
                    "body": "NABL",
                    "status": "Accredited",
                    "certificate_number": "TC-1234",
                    "valid_from": "2023-01-01",
                    "valid_until": "2025-12-31",
                    "scope_available": True,
                    "scope_document": "https://example.com/scope_doc.pdf"
                },
                "testing_capability": {
                    "standard": is_number,
                    "compatible": True,
                    "tests_supported": [
                        {"name": "Vacuum Retention", "clause": "7.1", "supported": True},
                        {"name": "Drop & Impact Test", "clause": "7.4", "supported": True}
                    ]
                },
                "turnaround": {
                    "min_days": 2,
                    "max_days": 10,
                    "unit": "working_days"
                },
                "availability": {
                    "status": "available",
                    "label": "Slots Available",
                    "capacity": "high"
                },
                "sample_submission": {
                    "required": True,
                    "method": "Request Sample Dispatch"
                },
                "actions": {
                    "book_test": "/book/lab_001"
                }
            }
        ]
    }

@app.get("/sample-tracking/{sample_id}")
async def get_sample_tracking(sample_id: str):
    """
    Roadmap/tracker endpoint for a submitted testing sample.
    """
    return {
        "sample_tracking": {
            "sample_id": sample_id,
            "overall_status": "in_progress",
            "steps": [
                {
                    "id": 1,
                    "title": "Sample Collection & Dispatch",
                    "status": "completed",
                    "completed_at": "2023-10-12T09:00:00Z"
                },
                {
                    "id": 2,
                    "title": "Testing & Quality Assurance",
                    "status": "in_progress",
                    "started_at": "2023-10-15T14:30:00Z"
                },
                {
                    "id": 3,
                    "title": "Dispatch & Transit Tracking",
                    "status": "pending"
                },
                {
                    "id": 4,
                    "title": "Test Report Verification on LIMS",
                    "status": "pending"
                }
            ]
        }
    }
