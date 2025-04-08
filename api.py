import os
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Body, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
import jwt
import datetime
import uuid
import json
from pydantic import BaseModel
from db import get_db_connection, save_document, get_document_by_id
from document_generator import generate_document_content
from rai import analyze_document
from payments import process_payment, create_subscription

# Create FastAPI app
app = FastAPI(title="DocGenius Lite API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "docgenius_lite_secret_key")
JWT_ALGORITHM = "HS256"

# Models
class DocumentRequest(BaseModel):
    doc_type: str
    title: str
    parameters: Dict[str, Any]

class PaymentRequest(BaseModel):
    token: str
    amount: float
    document_id: Optional[str] = None
    payment_type: str  # "document" or "subscription"

# Helper functions
def verify_token(authorization: str = Header(None)):
    """Verify JWT token from Authorization header"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.post("/api/documents")
async def create_document(
    request: DocumentRequest,
    user: dict = Depends(verify_token)
):
    """Generate and save a new document"""
    try:
        # Generate document content
        content = generate_document_content(request.doc_type, request.parameters)
        
        # Analyze document for RAI metrics
        rai_results = analyze_document(content, request.doc_type)
        
        # Save document to database
        doc_id = save_document(
            user_id=user["user_id"],
            doc_type=request.doc_type,
            title=request.title,
            content=content,
            parameters=json.dumps(request.parameters),
            rai_score=rai_results["score"],
            rai_flags=json.dumps(rai_results["flags"])
        )
        
        return {
            "status": "success",
            "document_id": doc_id,
            "rai_score": rai_results["score"],
            "rai_flags": rai_results["flags"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents/{doc_id}")
async def get_document(
    doc_id: str,
    user: dict = Depends(verify_token)
):
    """Retrieve a document by ID"""
    document = get_document_by_id(doc_id, user["user_id"])
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {
        "id": document[0],
        "doc_type": document[1],
        "title": document[2],
        "content": document[3],
        "parameters": json.loads(document[4]),
        "rai_score": document[5],
        "rai_flags": json.loads(document[6]),
        "created_at": document[7].isoformat()
    }

@app.post("/api/payments")
async def create_payment(
    request: PaymentRequest,
    user: dict = Depends(verify_token)
):
    """Process a payment for document purchase or subscription"""
    try:
        if request.payment_type == "document":
            # Process one-time document payment
            if not request.document_id:
                raise HTTPException(status_code=400, detail="Document ID required")
            
            payment_id = process_payment(
                user_id=user["user_id"],
                token=request.token,
                amount=request.amount,
                document_id=request.document_id
            )
            
            return {"status": "success", "payment_id": payment_id}
        
        elif request.payment_type == "subscription":
            # Process subscription payment
            subscription_id = create_subscription(
                user_id=user["user_id"],
                token=request.token,
                plan="pro"
            )
            
            # Update user's subscription in database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET subscription = 'pro' WHERE id = %s",
                (user["user_id"],)
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            return {"status": "success", "subscription_id": subscription_id}
        
        else:
            raise HTTPException(status_code=400, detail="Invalid payment type")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the API server if executed directly
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)
