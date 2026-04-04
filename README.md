# Delivery Routing System

A production-grade delivery routing backend inspired by Swiggy/Zomato — built with FastAPI, Kafka, Supabase, and Next.js. Features real-time driver assignment, surge pricing, route optimization, and JWT authentication.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Message Queue | Apache Kafka |
| Database | Supabase (PostgreSQL) |
| ORM | SQLAlchemy |
| Routing | OSRM (Open Source Routing Machine) |
| Real-time | WebSockets |
| Auth | JWT (python-jose + bcrypt) |
| Frontend | Next.js + Tailwind CSS |
| Maps | Leaflet.js + OpenStreetMap |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
Martensite/
├── backend/
│   ├── consumers/
│   │   └── order_consumer.py       # Kafka consumer — auto-assigns drivers
│   ├── middleware/
│   │   └── auth_middleware.py      # JWT token validation
│   ├── models/
│   │   ├── driver.py               # SQLAlchemy ORM + Pydantic schemas
│   │   ├── order.py                # Order model with surge pricing
│   │   └── user.py                 # User model for auth
│   ├── routers/
│   │   ├── auth.py                 # /auth/register, /auth/login
│   │   ├── drivers.py              # Driver CRUD + assignment
│   │   ├── orders.py               # Order management
│   │   ├── ratings.py              # Driver rating system
│   │   └── routes.py               # Route optimization + surge
│   ├── services/
│   │   ├── assignment.py           # Min Heap driver assignment
│   │   ├── auth_service.py         # JWT creation + verification
│   │   ├── distance.py             # OSRM + Haversine distance
│   │   ├── driver_store.py         # DB queries for drivers
│   │   ├── kafka_producer.py       # Kafka event publishers
│   │   ├── location_history.py     # Circular buffer for GPS history
│   │   ├── order_service.py        # Order status state machine
│   │   ├── rating_service.py       # Running average ratings
│   │   ├── route_optimizer.py      # TSP route optimization
│   │   └── surge_service.py        # Sliding window surge pricing
│   ├── db.py
│   ├── init_db.py
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── login/page.tsx
│   │   └── dashboard/page.tsx
│   ├── components/
│   │   ├── Map.tsx
│   │   ├── OrderBoard.tsx
│   │   ├── DriverList.tsx
│   │   └── SurgeIndicator.tsx
│   └── lib/
│       └── api.ts
└── docker-compose.yml
```

---

## System Architecture

```mermaid
graph TB
    subgraph ClientLayer["Client Layer"]
        FE["Next.js Dashboard"]
        WS_CLIENT["WebSocket Client"]
    end

    subgraph APILayer["API Layer - FastAPI"]
        AUTH["auth router"]
        ORDERS["orders router"]
        DRIVERS["drivers router"]
        RATINGS["ratings router"]
        ROUTES["routes router"]
        WS["WebSocket endpoint"]
    end

    subgraph QueueLayer["Message Queue - Kafka"]
        T1["new-orders topic"]
        T2["driver-assignments topic"]
        T3["order-status-updates topic"]
    end

    subgraph ServicesLayer["Services Layer"]
        ASSIGN["Assignment Service"]
        SURGE["Surge Calculator"]
        STATE["State Machine"]
        OPTIMIZER["Route Optimizer"]
        HISTORY["Location History"]
    end

    subgraph DataLayer["Data Layer"]
        SUPABASE[("Supabase PostgreSQL")]
        MEMORY["In-Memory Store"]
    end

    subgraph ExternalLayer["External APIs"]
        OSRM["OSRM Routing API"]
    end

    FE -->|"HTTP + JWT"| AUTH
    FE -->|"HTTP + JWT"| ORDERS
    FE -->|HTTP| DRIVERS
    FE -->|HTTP| RATINGS
    FE -->|HTTP| ROUTES
    WS_CLIENT -->|WebSocket| WS

    ORDERS -->|publish| T1
    T1 -->|consume| ASSIGN
    ASSIGN -->|publish| T2
    STATE -->|publish| T3

    ASSIGN -->|driving distance| OSRM
    ASSIGN --> SURGE
    DRIVERS --> MEMORY
    ORDERS --> SUPABASE
    AUTH --> SUPABASE
    WS --> HISTORY
    WS --> MEMORY
```

---

## Order Lifecycle Flow

```mermaid
sequenceDiagram
    participant C as Customer
    participant API as FastAPI
    participant K as Kafka
    participant CS as Consumer
    participant DS as Driver Store
    participant DB as Supabase
    participant D as Driver App

    C->>API: POST /orders/ with JWT token
    API->>API: Calculate surge multiplier
    API->>DB: Save order with status pending
    API->>K: Publish to new-orders topic
    API-->>C: Return order with price

    K->>CS: Consume new order event
    CS->>DS: get_available_drivers()
    DS->>DB: Query available drivers
    DB-->>DS: Return drivers list
    CS->>CS: Min Heap finds nearest driver
    CS->>DB: Update order status to assigned
    CS->>DS: Mark driver as ON_TRIP
    CS->>K: Publish to driver-assignments topic

    D->>API: WebSocket connect
    D->>API: Stream GPS coordinates
    API->>DS: update_driver_location()
    API->>API: Record in circular buffer
    API-->>D: Acknowledge update

    C->>API: PATCH status to picked_up
    API->>API: Validate via state machine
    API->>DB: Update order status
    API->>K: Publish status update
    API-->>C: Return updated order

    C->>API: PATCH status to delivered
    API->>DB: Final status update
    C->>API: POST /ratings/ to rate driver
    API->>DB: Update running average rating
```

---

## Driver Assignment Algorithm

```mermaid
flowchart TD
    A["New Order Created"] --> B["Get all available drivers from DB"]
    B --> C{"Any drivers available?"}
    C -->|No| D["Return 503 No drivers available"]
    C -->|Yes| E["Calculate straight-line distance for ALL drivers"]

    E --> F["Build Min Heap\nScore = distance minus rating x 0.1\nBuild time O(n)"]

    F --> G["Pop top 3 candidates from heap\nO(log n) per pop"]

    G --> H["Call OSRM for real driving distance\non top 3 candidates only"]

    H --> I["Sort by actual driving distance"]
    I --> J["Pick winner - nearest driver"]

    J --> K["Mark driver ON_TRIP in DB\nprevents double assignment"]
    K --> L["Calculate final price\nbase + distance fee x surge multiplier"]
    L --> M["Return AssignmentResult to caller"]
```

---

## Surge Pricing — Sliding Window

```mermaid
flowchart TD
    A["New order arrives at pickup zone"] --> B["Add timestamp to zone deque"]
    B --> C["Remove timestamps older than 10 minutes"]
    C --> D["Count remaining events in window"]

    D --> E["demand = recent order count\nsupply = available drivers in zone"]
    E --> F["ratio = demand divided by supply"]

    F --> G{"What is the ratio?"}
    G -->|"ratio >= 4"| H["Surge = 2.5x"]
    G -->|"ratio >= 3"| I["Surge = 2.0x"]
    G -->|"ratio >= 2"| J["Surge = 1.5x"]
    G -->|"ratio >= 1"| K["Surge = 1.2x"]
    G -->|"ratio below 1"| L["Surge = 1.0x normal pricing"]

    H --> M["Apply multiplier to order price"]
    I --> M
    J --> M
    K --> M
    L --> M
```

---

## Order State Machine — Directed Graph

```mermaid
stateDiagram-v2
    [*] --> pending : Order Created

    pending --> assigned : Driver auto-assigned by Kafka consumer
    pending --> cancelled : Customer cancels before assignment

    assigned --> picked_up : Driver picks up the order
    assigned --> cancelled : Driver cancels the trip

    picked_up --> in_transit : Order is on the way

    in_transit --> delivered : Order successfully delivered

    delivered --> [*]
    cancelled --> [*]
```

---

## Route Optimization — TSP

```mermaid
flowchart TD
    A["Driver location plus N delivery stops"] --> B{"N is 8 stops or fewer?"}

    B -->|Yes - small set| C["Brute Force TSP\nTry every permutation\nTime complexity O(n factorial)"]
    B -->|No - large set| D["Nearest Neighbor Heuristic\nGreedy approach\nTime complexity O(n squared)"]

    C --> E["Calculate total distance for each permutation"]
    E --> F["Select permutation with minimum total distance"]

    D --> G["Start from current driver location"]
    G --> H["Find nearest unvisited stop"]
    H --> I["Travel to that stop"]
    I --> J{"More unvisited stops?"}
    J -->|Yes| H
    J -->|No| K["Greedy route complete"]

    F --> L["Return optimized route and total km"]
    K --> L
```

---

## Driver Rating — Running Average

```mermaid
flowchart LR
    A["Customer submits rating\nexample: 4.5 stars"] --> B["Fetch driver from DB\ncurrent avg = 4.8\ntotal ratings = 10"]

    B --> C["Compute new average\ncurrent_avg x total + new_rating\ndivided by total + 1\n\nResult = 4.77"]

    C --> D["Save to DB\nrating = 4.77\ntotal_ratings = 11"]

    D --> E["Influences next assignment\nscore = distance minus rating x 0.1\nhigher rated drivers preferred"]
```

---

## JWT Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant API as FastAPI
    participant DB as Supabase
    participant MW as Auth Middleware

    U->>API: POST /auth/register with email and password
    API->>API: Hash password with bcrypt
    API->>DB: INSERT INTO users table
    API->>API: Create JWT with user_id and role as claims
    API-->>U: Return access_token and user info

    U->>API: POST /auth/login with credentials
    API->>DB: SELECT user WHERE email matches
    API->>API: Verify password against bcrypt hash
    API->>API: Create JWT token
    API-->>U: Return access_token and user info

    U->>API: POST /orders/ with Authorization Bearer token
    API->>MW: Extract and validate token
    MW->>MW: Decode JWT and verify signature
    MW->>DB: Fetch user by id from token claims
    MW-->>API: Inject current_user into route handler
    API->>DB: INSERT new order
    API-->>U: Order created successfully
```

---

## WebSocket Real-Time Location

```mermaid
sequenceDiagram
    participant D as Driver App
    participant WS as WebSocket Server
    participant MEM as Driver Store
    participant BUF as Circular Buffer

    D->>WS: Connect to ws://api/drivers/ws/driver_id
    WS-->>D: Connection accepted
    WS->>MEM: Register active connection for driver_id

    loop Continuous GPS stream
        D->>WS: Send lat and lng coordinates as JSON
        WS->>MEM: Update driver location in database
        WS->>BUF: Record in circular buffer - max 100 points per driver
        WS-->>D: Acknowledge with updated position
    end

    D->>WS: Client disconnects
    WS->>MEM: Remove driver from active connections
```

---

## Docker Architecture

```mermaid
graph TB
    subgraph DockerCompose["Docker Compose - Local Development"]
        subgraph KafkaStack["Kafka Stack"]
            ZK["Zookeeper - port 2181"]
            KF["Kafka - port 9092"]
            ZK --> KF
        end

        subgraph AppStack["Application"]
            BE["FastAPI Backend - port 8001"]
            RD["Redis - port 6379"]
        end

        KF --> BE
        RD --> BE
    end

    subgraph CloudServices["External Cloud Services"]
        SB[("Supabase PostgreSQL")]
        OSRM_EXT["OSRM Routing API"]
    end

    BE --> SB
    BE --> OSRM_EXT

    subgraph Production["Production Deployment"]
        RENDER["Render - Backend API"]
        VERCEL["Vercel - Next.js Frontend"]
        VERCEL -->|"HTTPS API requests"| RENDER
        RENDER --> SB
    end
```

---

## Data Structures Used

| Feature | Data Structure | Complexity |
|---------|---------------|------------|
| Driver Assignment | Min Heap | O(log n) nearest driver lookup |
| Order Status | Directed Graph | O(1) edge lookup for valid transitions |
| Surge Pricing | Sliding Window deque | O(1) add and remove |
| Location History | Circular Buffer deque maxlen | O(1) append, auto-evicts old data |
| Route Optimization | TSP and Nearest Neighbor | O(n!) brute force or O(n^2) heuristic |
| Rating System | Running Average | O(1) update without storing all ratings |
| Active WebSockets | Hash Map | O(1) driver lookup by ID |

---

## Getting Started

### Prerequisites
- Python 3.13+
- Node.js 18+
- Docker + Docker Compose
- Supabase account

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Fill in DATABASE_URL, SECRET_KEY, KAFKA_BOOTSTRAP_SERVERS

python init_db.py
uvicorn main:app --reload --port 8001
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Set NEXT_PUBLIC_API_URL=http://localhost:8001
npm run dev
```

### Docker Full Stack
```bash
docker-compose up --build
```

---

## API Reference

| Method | Endpoint | Auth Required | Description |
|--------|----------|--------------|-------------|
| POST | `/auth/register` | No | Register new user |
| POST | `/auth/login` | No | Login and get JWT token |
| POST | `/orders/` | Yes | Create a new order |
| GET | `/orders/` | Yes | List all orders |
| PATCH | `/orders/{id}/status` | Yes | Update order status |
| POST | `/drivers/register` | No | Register a driver |
| POST | `/drivers/assign` | No | Assign nearest available driver |
| GET | `/drivers/` | No | List all drivers |
| POST | `/ratings/` | No | Submit driver rating |
| GET | `/ratings/top-drivers` | No | Get top rated drivers |
| POST | `/routes/optimize` | No | Optimize multi-stop route |
| POST | `/routes/surge` | No | Get current surge multiplier |
| WS | `/drivers/ws/{id}` | No | Real-time GPS location stream |

Full interactive docs at `http://localhost:8001/docs`

---

## Deployment

| Service | Platform | Notes |
|---------|----------|-------|
| Backend API | Render | Free tier, auto-deploy from GitHub |
| Frontend | Vercel | One-click Next.js deployment |
| Database | Supabase | Managed PostgreSQL, free tier |

---

## Built By

Raj Aryan

Inspired by the engineering systems behind Swiggy, Zomato, and Uber Eats.