from fastapi import FastAPI
 
from project.db import create_db_and_tables
from project.app.router import router as api_router


app = FastAPI()  


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(api_router, prefix="/api")