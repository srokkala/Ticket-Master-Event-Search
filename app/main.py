from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import events

app = FastAPI(title="TickerMaster Event Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the TicketMaster Event Search API"}