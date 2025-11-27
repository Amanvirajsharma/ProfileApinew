from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import profile

# FastAPI app banao
app = FastAPI(
    title="Profile API 🚀",
    description="""
    ## Profile Management API
    
    Ye API profiles manage karne ke liye hai.
    
    ### Features:
    - ✨ Create Profile
    - 📋 Get All Profiles (with pagination)
    - 👤 Get Single Profile
    - ✏️ Update Profile
    - 🗑️ Delete Profile
    - 🔍 Search Profiles
    
    ### Made with ❤️ using FastAPI + Supabase
    """,
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# CORS Middleware - Client access ke liye zaroori hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein specific domains dalo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes include karo
app.include_router(profile.router, prefix="/api/v1")


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to Profile API! 🚀",
        "docs": "/docs",
        "health": "/health"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy ✅",
        "message": "API chal raha hai bhai!"
    }