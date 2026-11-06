from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import videos
from db import create_all_table

app = FastAPI(lifespan=create_all_table)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500", 
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://oliverpagina.s3-website-us-east-1.amazonaws.com"
    ],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(videos.router)

@app.get("/")
def root():
    return {"hello": "world"}