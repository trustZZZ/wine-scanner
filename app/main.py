import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from app.messanger.router import router as chat_router
from app.pages.router import router as pages_router
from app.users.router import router as user_router
from app.search.router import router as search_router
app = FastAPI()

app.include_router(user_router)
app.include_router(pages_router)
app.include_router(chat_router)
app.include_router(search_router)


# Подключение CORS, чтобы запросы к API могли приходить из браузера

origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"]
)


# @app.on_event("startup")
# def startup():
#     redis = aioredis.from_url("redis://localhost:6379", encoding='utf-8', decode_response=True)
#     FastAPICache.init(RedisBackend(redis), prefix="cache")


if __name__ == '__main__':
    uvicorn.run('app.main:app', host="localhost", env_file='.env', port=3000, reload=True)

