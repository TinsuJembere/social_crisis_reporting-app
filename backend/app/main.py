from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Community Crisis Reporting & Response Platform API",
    description="Backend API for reporting and managing community issues",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Community Crisis Reporting & Response Platform API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import routers
from app.routers import auth, issues, images, notifications
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(issues.router, prefix="/api/issues", tags=["issues"])
app.include_router(images.router, prefix="/api/images", tags=["images"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["notifications"])

# Will be created in next steps
# from app.routers import users
# app.include_router(users.router, prefix="/api/users", tags=["users"])

