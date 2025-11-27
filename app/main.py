from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import profile

app = FastAPI(
    title="Profile API",
    description="Profile Management API with Supabase",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(profile.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Welcome to Profile API!",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is running!"}