from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import data_router

app = FastAPI(
    title="Water Segmentation API",
    description="API for detecting and segmenting water bodies in images",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data_router)

@app.get("/")
async def root():
    return {"message": "Water Segmentation API is running"}

