"""Main module"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

FASTAPI_ROOT_PATH = os.getenv('FASTAPI_ROOT_PATH', "")
app = FastAPI(root_path=FASTAPI_ROOT_PATH)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def main():
    """Default API Root

    Returns:
        string: Basic string response
    """
    return "Hello, this message comes from the Fast API root endpoint!"
