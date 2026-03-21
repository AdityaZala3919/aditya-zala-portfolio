from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()


async def verify_master_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verify that the provided token matches the MASTER_TOKEN environment variable.
    All endpoints require this authentication.
    """
    master_token = os.getenv("MASTER_TOKEN", "your-secret-master-token")
    
    if credentials.credentials != master_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing master token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return credentials.credentials
