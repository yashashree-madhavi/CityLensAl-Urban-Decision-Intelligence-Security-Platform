from fastapi import FastAPI, Depends
from sqlalchemy import text

from app.models.user import User
from app.models.emergency import Emergency
from app.database.database import Base, engine
from app.routes.auth import router as auth_router
from app.routes.emergency import router as emergency_router
from app.security.auth import get_current_user, require_role
from app.websocket.connection import router as websocket_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CityLens AI",
    description="AI-Powered Urban Decision Intelligence Platform for Mumbai",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(emergency_router)
app.include_router(websocket_router)

@app.get("/")
def root():
    return {
        "message": "CityLens AI Backend is running 🚀"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/database-test")
def database_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return {
                "database": "connected",
                "result": result.scalar()
            }

    except Exception as e:
        return {
            "database": "connection failed",
            "error": str(e)
        }

@app.get("/protected-test")
def protected_test(
    current_user: User = Depends(get_current_user)
):
    return {
        "message": "You are authenticated!",
        "user_id": current_user.id,
        "name": current_user.name,
        "role": current_user.role
    }

@app.get("/admin-test")
def admin_test(
    current_user: User = Depends(require_role("admin"))
):
    return {
        "message": "Welcome Admin!",
        "user_id": current_user.id,
        "name": current_user.name,
        "role": current_user.role
    }