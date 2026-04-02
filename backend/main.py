# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from db import engine, Base
# from routers import orders, drivers

# # Create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Delivery Routing System")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(orders.router)
# app.include_router(drivers.router)

# @app.get("/")
# def root():
#     return {"message": "Delivery Routing System API running!"}

# @app.get("/health")
# def health():
#     return {"status": "healthy"}

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from db import engine, Base
# from routers import orders, drivers
# from consumers import start_consumer_thread

# # Create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Delivery Routing System")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(orders.router)
# app.include_router(drivers.router)

# @app.on_event("startup")
# def startup_event():
#     start_consumer_thread()
#     print("🚀 Delivery Routing System started!")

# @app.get("/")
# def root():
#     return {"message": "Delivery Routing System API running!"}

# @app.get("/health")
# def health():
#     return {"status": "healthy"}


# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.middleware.cors import CORSMiddleware
# from db import engine, Base
# from routers import orders, drivers
# from consumers import start_consumer_thread
# from services import driver_store
# import json

# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Delivery Routing System")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(orders.router)
# app.include_router(drivers.router)

# active_connections: dict[str, WebSocket] = {}

# # ── WebSocket here to avoid route conflict with /{driver_id}/status ──────────
# @app.websocket("/drivers/ws/{driver_id}")
# async def driver_location_ws(websocket: WebSocket, driver_id: str):
#     await websocket.accept()
#     active_connections[driver_id] = websocket
#     print(f"🟢 Driver {driver_id} connected")
#     try:
#         while True:
#             data = await websocket.receive_text()
#             location = json.loads(data)
#             driver_store.update_driver_location(
#                 driver_id, location["lat"], location["lng"]
#             )
#             await websocket.send_text(json.dumps({
#                 "status": "updated",
#                 "driver_id": driver_id,
#                 "lat": location["lat"],
#                 "lng": location["lng"],
#             }))
#     except WebSocketDisconnect:
#         active_connections.pop(driver_id, None)
#         print(f"🔴 Driver {driver_id} disconnected")

# @app.on_event("startup")
# def startup_event():
#     start_consumer_thread()
#     print("🚀 Delivery Routing System started!")

# @app.get("/")
# def root():
#     return {"message": "Delivery Routing System API running!"}

# @app.get("/health")
# def health():
#     return {"status": "healthy"}

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base
from routers import orders, drivers
from routers.ratings import router as ratings_router
from routers.routes import router as routes_router
from consumers import start_consumer_thread
from services import driver_store
from services.location_history import location_history
import json

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
app.include_router(ratings_router)
app.include_router(routes_router)

active_connections: dict[str, WebSocket] = {}

@app.websocket("/drivers/ws/{driver_id}")
async def driver_location_ws(websocket: WebSocket, driver_id: str):
    await websocket.accept()
    active_connections[driver_id] = websocket
    print(f"🟢 Driver {driver_id} connected")
    try:
        while True:
            data     = await websocket.receive_text()
            location = json.loads(data)

            # Update DB
            driver_store.update_driver_location(
                driver_id, location["lat"], location["lng"]
            )
            # Store in circular buffer
            location_history.record(
                driver_id, location["lat"], location["lng"]
            )

            await websocket.send_text(json.dumps({
                "status":    "updated",
                "driver_id": driver_id,
                "lat":       location["lat"],
                "lng":       location["lng"],
            }))
    except WebSocketDisconnect:
        active_connections.pop(driver_id, None)
        print(f"🔴 Driver {driver_id} disconnected")

@app.on_event("startup")
def startup_event():
    start_consumer_thread()
    print("🚀 Delivery Routing System started!")

@app.get("/")
def root():
    return {"message": "Delivery Routing System API running!"}

@app.get("/health")
def health():
    return {"status": "healthy"}