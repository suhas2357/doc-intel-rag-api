from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.rag import router as rag_router

app = FastAPI(
    title="Advanced RAG FastAPI App",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://doc-intel-rag-frontend-vwlf.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rag_router, prefix="/rag", tags=["RAG"])


@app.get("/")
def root():
    return {
        "message": "Advanced RAG FastAPI App is running"
    }