from sys import prefix
from fastapi import APIRouter
from app.api.api_v1.endpoints import  api_users, api_channels, api_confessions
api_router = APIRouter()
# api_router.include_router(login.router, tags=["login"])
api_router.include_router(api_users.router, prefix="/users", tags=["users"])
api_router.include_router(api_channels.router, prefix="/channels", tags=["channels"])
api_router.include_router(api_confessions.router, prefix="/confessions", tags=["confessions"])









#api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
#api_router.include_router(items.router, prefix="/items", tags=["items"])
