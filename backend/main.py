from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base
from routers import orders, drivers

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Delivery Routing System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router)
app.include_router(drivers.router)

@app.get("/")
def root():
    return {"message": "Delivery Routing System API running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}