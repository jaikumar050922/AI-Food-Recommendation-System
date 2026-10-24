import os
from typing import List
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "NutriAI Backend API"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Security & JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "nutriai-production-secret-key-change-in-env-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # Allowed CORS Origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "https://*.vercel.app",
        "*"
    ]
    
    # Foods dataset path
    DATA_PATH: str = os.getenv(
        "DATA_PATH", 
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "foods.csv")
    )

settings = Settings()
