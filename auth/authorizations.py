import asyncio
from functools import wraps
from fastapi import HTTPException

def authorize(role: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if current_user is None:
                raise HTTPException(status_code=401, detail="User is not authenticated")
            
            user_role = getattr(current_user, "rol", None)  # Assuming 'role' attribute
            if user_role not in role:
                raise HTTPException(status_code=403, detail="User is not authorized to access")
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator