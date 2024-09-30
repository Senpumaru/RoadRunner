# app/dependencies.py
from fastapi import Depends, HTTPException, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.user import User
from typing import Optional
import logging

logger = logging.getLogger(__name__)

async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_current_user(x_token: str = Header(...), db: AsyncSession = Depends(get_db)):
    user = await db.get(User, {"token": x_token})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)):
        if user.role not in self.allowed_roles:
            logger.warning(f"User {user.id} with role {user.role} tried to access a restricted resource")
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return user

async def log_request(request: Request, user: User = Depends(get_current_user)):
    logger.info(f"Request to {request.url.path} by user {user.id}")
    return request