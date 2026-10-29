from fastapi import FastAPI
from app.api.routes.rag import router as rag_router

app = FastAPI(
    title="Advanced RAG FastAPI App",
    version="1.0.0"
)

app.include_router(rag_router, prefix="/rag", tags=["RAG"])


@app.get("/")
def root():
    return {
        "message": "Advanced RAG FastAPI App is running"
    }