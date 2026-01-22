from fastapi import FastAPI
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware

from  agent import app


fast = FastAPI(
    title="Travel / Product Support Agent",
    version="0.1",
    description="LangGraph + Django product search",
)

fast.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:8000",      # your Django dev server
        "http://127.0.0.1:8000",      # sometimes needed
        "http://localhost:3000",      # if using Vite/React dev server
        "*"
    ],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],

)

add_routes(
    fast,
    app,
    path="/agent",
    config_keys=["configurable"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fast, host="0.0.0.0", port=8123)








