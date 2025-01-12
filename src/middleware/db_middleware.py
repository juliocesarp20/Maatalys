from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.db.session import get_async_session


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with get_async_session() as session:
            request.state.db = session
            response = await call_next(request)
        return response
