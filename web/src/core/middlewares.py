from starlette.middleware.base import BaseHTTPMiddleware


class ProxyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.scope["scheme"] = "https"
        response = await call_next(request)
        return response


