from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import categories

# FastAPIアプリケーションのインスタンス化
app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
