from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import data_router, base_router

app = FastAPI()
app.include_router(base_router)
app.include_router(data_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


