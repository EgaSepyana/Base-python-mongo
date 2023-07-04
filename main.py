from fastapi import FastAPI
import os
from src.controller import role_controller
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Python Template Management" , description="Template Management For Python")

@app.get("/ping")
def Root():
    return {"massage" : "pong"}

app.include_router(role_controller.NewRoleController().GetRouter())

if __name__ == "__main__":
    port = os.getenv("SERVICE_PORT")
    if not port:
        port="8000"
    uvicorn.run(app, host="0.0.0.0", port=int(port))