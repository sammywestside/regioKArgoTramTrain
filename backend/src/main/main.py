from fastapi import FastAPI
import uvicorn
from src.main.controller import train_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(train_controller.router, prefix="/api", tags=["Route"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
