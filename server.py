from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import subprocess
import logging
import os
import sys
import uvicorn 

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import classifier
try:
    from shared.intent_classifier import get_intent_classifier
    classifier = get_intent_classifier(use_llm=True)
except Exception as e:
    print(f"Warning: Could not load intent classifier: {e}")
    classifier = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    result: str
    intent: str = ""
    confidence: float = 0.0

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directories FIRST (before routes)
if os.path.exists("public"):
    app.mount("/public", StaticFiles(directory="public"), name="public")

if os.path.exists("src"):
    app.mount("/src", StaticFiles(directory="src"), name="src")
    
if os.path.exists("shared"):
    app.mount("/shared", StaticFiles(directory="shared"), name="shared")

# If using Vite build
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

# API Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "AIDA Chatbot API",
        "classifier": "enabled" if classifier else "disabled"
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint with intent routing"""
    query = request.message
    
    if not query:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    logger.info(f"Query: {query}")
    
    # Default values
    intent = "knowledge-bps"
    confidence = 0.5
    
    # Classify intent
    if classifier:
        try:
            classification = classifier.classify(query)
            intent = classification.get("intent", "knowledge-bps")
            confidence = classification.get("confidence", 0.5)
            logger.info(f"Intent: {intent} (confidence: {confidence})")
        except Exception as e:
            logger.error(f"Classification error: {e}")
    
    # Route based on intent
    try:
        if intent == "permintaan-data":
            # Call Semantic Parsing
            logger.info("Routing to Semantic Parsing")
            result = subprocess.run(
                ["python", "semantic-parsing/chatbot_semantic.py", query],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
        elif intent == "knowledge-bps":
            # Call RAG
            logger.info("Routing to RAG")
            result = subprocess.run(
                ["python", "rag-data/query_data.py", query],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
        else:
            # Handle 'other' intent
            return ChatResponse(
                result="Maaf, saya tidak dapat memahami pertanyaan Anda. Silakan coba pertanyaan tentang data statistik atau informasi BPS.",
                intent=intent,
                confidence=confidence
            )
        
        # Check subprocess result
        if result.returncode != 0:
            logger.error(f"Module error: {result.stderr}")
            raise HTTPException(status_code=500, detail="Error processing query")
        
        response_text = result.stdout.strip() or "Maaf, tidak ada jawaban yang dapat diberikan."
        
        return ChatResponse(
            result=response_text,
            intent=intent,
            confidence=confidence
        )
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve Frontend - MUST BE LAST (catch-all route)
@app.get("/")
async def serve_frontend():
    """Serve the main index.html"""
    # Check if we have a built version
    if os.path.exists('dist/index.html'):
        return FileResponse('dist/index.html')
    elif os.path.exists('index.html'):
        return FileResponse('index.html')
    else:
        return {"error": "Frontend not found. Make sure index.html exists"}

# Catch all routes for SPA (Single Page Application)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Catch all routes to serve SPA"""
    # Skip API routes
    if full_path.startswith("api/") or full_path.startswith("chat") or full_path.startswith("health"):
        raise HTTPException(status_code=404, detail="Not found")
    
    # Try to serve the requested file
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return FileResponse(full_path)
    
    # Try in dist folder
    dist_path = f"dist/{full_path}"
    if os.path.exists(dist_path) and os.path.isfile(dist_path):
        return FileResponse(dist_path)
    
    # For SPA, always return index.html for client-side routing
    if os.path.exists('dist/index.html'):
        return FileResponse('dist/index.html')
    elif os.path.exists('index.html'):
        return FileResponse('index.html')
    else:
        raise HTTPException(status_code=404, detail="Not found")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)