"""
Backend startup script
Run from root directory: python backend/run.py
"""
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file in root directory
load_dotenv()

if __name__ == "__main__":
    master_token = os.getenv("MASTER_TOKEN", "your-secret-master-token")
    print(f"Starting backend with MASTER_TOKEN: {master_token[:10]}...")
    
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
