# 🚀 Delivery Routing System

A production-grade delivery routing backend inspired by Swiggy/Zomato — built with FastAPI, Kafka, Supabase, and Next.js. Features real-time driver assignment, surge pricing, route optimization, and JWT authentication.

---

## 📦 Tech Stack

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

## 🗂️ Project Structure

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
│   ├── schemas/
│   │   └── order.py                # Pydantic request/response shapes
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
│   ├── db.py                       # SQLAlchemy engine + session
│   ├── init_db.py                  # Table creation script
│   ├── main.py                     # FastAPI app + WebSocket
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx                # Landing page
│   │   ├── login/page.tsx          # Auth page
│   │   └── dashboard/page.tsx      # Live dashboard
│   ├── components/
│   │   ├── Map.tsx                 # Leaflet driver map
│   │   ├── OrderBoard.tsx          # Live order list
│   │   ├── DriverList.tsx          # Driver status board
│   │   └── SurgeIndicator.tsx      # Surge multiplier display
│   └── lib/
│       └── api.ts                  # Axios API client
└── docker-compose.yml
```

---

## 🔄 System Architecture

```mermaid
graph TB
    subgraph Client["🖥️ Client Layer"]
        FE[Next.js Dashboard]
        WS_CLIENT[WebSocket Client]
    end

    subgraph API["⚡ API Layer - FastAPI"]
        AUTH[/auth]
        ORDERS[/orders]
        DRIVERS[/drivers]
        RATINGS[/ratings]
        ROUTES[/routes]
        WS[WebSocket /drivers/ws]
    end

    subgraph Queue["📨 Message Queue - Kafka"]
        T1[new-orders topic]
        T2[driver-assignments topic]
        T3[order-status-updates topic]
    end

    subgraph Services["🔧 Services Layer"]
        ASSIGN[Assignment Service]
        SURGE[Surge Calculator]
        STATE[State Machine]
        OPTIMIZER[Route Optimizer]
        HISTORY[Location History]
    end

    subgraph DB["🗄️ Data Layer"]
        SUPABASE[(Supabase PostgreSQL)]
        MEMORY[In-Memory Store]
    end

    subgraph External["🌐 External APIs"]
        OSRM[OSRM Routing API]
    end

    FE -->|HTTP + JWT| AUTH
    FE -->|HTTP + JWT| ORDERS
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

## 🚦 Order Lifecycle Flow

```mermaid
sequenceDiagram
    participant C as Customer
    participant API as FastAPI
    participant K as Kafka
    participant CS as Consumer
    participant DS as Driver Store
    participant DB as Supabase
    participant D as Driver App

    C->>API: POST /orders/ (with JWT)
    API->>API: Calculate surge multiplier
    API->>DB: Save order (status=pending)
    API->>K: Publish to new-orders topic
    API-->>C: Return order + price

    K->>CS: Consume new order event
    CS->>DS: get_available_drivers()
    DS->>DB: Query available drivers
    DB-->>DS: Return drivers list
    CS->>CS: Min Heap — find nearest driver
    CS->>DB: Update order (status=assigned, driver_id)
    CS->>DS: Mark driver ON_TRIP
    CS->>K: Publish to driver-assignments topic

    D->>API: WebSocket connect /drivers/ws/{id}
    D->>API: Stream GPS location
    API->>DS: update_driver_location()
    API->>API: Record in circular buffer
    API-->>D: Acknowledge update

    C->>API: PATCH /orders/{id}/status (picked_up)
    API->>API: Validate transition via state machine
    API->>DB: Update status
    API->>K: Publish to order-status-updates
    API-->>C: Updated order

    C->>API: PATCH /orders/{id}/status (delivered)
    API->>DB: Final status update
    C->>API: POST /ratings/ (rate driver)
    API->>DB: Update running average rating
```

---

## 🧠 Driver Assignment Algorithm

```mermaid
flowchart TD
    A[New Order Created] --> B[Get all available drivers from DB]
    B --> C{Any drivers available?}
    C -->|No| D[Return 503 — No drivers]
    C -->|Yes| E[Calculate straight-line distance\nfor ALL drivers — O·n·]

    E --> F[Build Min Heap\nScore = distance − rating×0.1\nO·n· to build]

    F --> G[Pop top 3 from heap\nO·log n· each]

    G --> H[Call OSRM for real driving\ndistance on top 3 only]

    H --> I[Sort by actual driving distance]
    I --> J[Pick winner]

    J --> K[Mark driver ON_TRIP\nin DB immediately]
    K --> L[Calculate final price\nbase + distance fee × surge]
    L --> M[Return AssignmentResult]

    style F fill:#1e40af,color:#fff
    style H fill:#065f46,color:#fff
    style K fill:#7c2d12,color:#fff
```

---

## 💰 Surge Pricing — Sliding Window

```mermaid
flowchart LR
    subgraph Window["⏱️ 10-Minute Sliding Window"]
        direction LR
        E1[Order t-9m] --> E2[Order t-7m] --> E3[Order t-4m] --> E4[Order t-1m]
    end

    subgraph Calc["📊 Surge Calculation"]
        DEMAND[demand = orders in window\n= 4]
        SUPPLY[supply = available drivers\n= 2]
        RATIO[ratio = demand ÷ supply\n= 2.0]
    end

    subgraph Tiers["💸 Surge Tiers"]
        T1["ratio ≥ 4 → 2.5x 🔴"]
        T2["ratio ≥ 3 → 2.0x 🟠"]
        T3["ratio ≥ 2 → 1.5x 🟡"]
        T4["ratio ≥ 1 → 1.2x 🟢"]
        T5["ratio < 1 → 1.0x ⚪"]
    end

    Window --> Calc
    RATIO -->|2.0 matches| T3

    style T3 fill:#92400e,color:#fff
```

---

## 📊 Order State Machine — Directed Graph

```mermaid
stateDiagram-v2
    [*] --> pending : Order Created

    pending --> assigned : Driver auto-assigned\nby Kafka consumer
    pending --> cancelled : Customer cancels

    assigned --> picked_up : Driver picks up order
    assigned --> cancelled : Driver cancels

    picked_up --> in_transit : Order on the way

    in_transit --> delivered : Order delivered ✅

    delivered --> [*]
    cancelled --> [*]

    note right of pending
        surge_multiplier calculated
        base_price set
        Kafka event published
    end note

    note right of assigned
        driver_id saved to DB
        driver status → ON_TRIP
        assignment event published
    end note
```

---

## 🗺️ Route Optimization — TSP

```mermaid
flowchart TD
    A[Driver + N delivery stops] --> B{N ≤ 8 stops?}

    B -->|Yes| C[Brute Force TSP\nTry all N! permutations\nO·n!·]
    B -->|No| D[Nearest Neighbor Heuristic\nGreedy approach\nO·n²·]

    C --> E[Calculate total distance\nfor each permutation]
    E --> F[Pick permutation with\nminimum total distance]

    D --> G[Start from driver location]
    G --> H[Find nearest unvisited stop]
    H --> I[Move to that stop]
    I --> J{More stops?}
    J -->|Yes| H
    J -->|No| K[Return greedy route]

    F --> L[Return optimized route + distance]
    K --> L

    style C fill:#1e3a5f,color:#fff
    style D fill:#1e3a5f,color:#fff
    style F fill:#14532d,color:#fff
    style K fill:#14532d,color:#fff
```

---

## ⭐ Driver Rating System — Running Average

```mermaid
flowchart LR
    A[Customer submits rating\ne.g. 4.5 ⭐] --> B[Fetch driver from DB\ncurrent_avg=4.8, total=10]

    B --> C["new_avg = \ncurrent_avg × total + new_rating\n÷ total + 1\n\n= 4.8×10 + 4.5 ÷ 11\n= 4.77"]

    C --> D[Save to DB\nrating=4.77\ntotal_ratings=11]

    D --> E[Affects next assignment\nscore = distance − rating×0.1]

    style C fill:#1e40af,color:#fff
    style E fill:#065f46,color:#fff
```

---

## 🔐 JWT Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant API as FastAPI
    participant DB as Supabase
    participant MW as Auth Middleware

    U->>API: POST /auth/register\n{email, password, name}
    API->>API: bcrypt.hash(password)
    API->>DB: INSERT INTO users
    API->>API: jwt.encode({sub: user_id, role})
    API-->>U: {access_token, user}

    U->>API: POST /auth/login\n{email, password}
    API->>DB: SELECT user WHERE email=?
    API->>API: bcrypt.verify(password, hash)
    API->>API: jwt.encode({sub: user_id})
    API-->>U: {access_token, user}

    U->>API: POST /orders/\nAuthorization: Bearer TOKEN
    API->>MW: Validate token
    MW->>MW: jwt.decode(token)
    MW->>DB: SELECT user WHERE id=sub
    MW-->>API: current_user injected
    API->>DB: INSERT order
    API-->>U: Order created ✅
```

---

## 📡 WebSocket Real-Time Location

```mermaid
sequenceDiagram
    participant D as Driver App
    participant WS as WebSocket Server
    participant MEM as In-Memory Store
    participant BUF as Circular Buffer

    D->>WS: Connect ws://api/drivers/ws/{driver_id}
    WS-->>D: Connection accepted ✅
    WS->>MEM: active_connections[driver_id] = ws

    loop Every few seconds
        D->>WS: {"lat": 12.975, "lng": 77.596}
        WS->>MEM: update_driver_location(lat, lng)
        WS->>BUF: location_history.record(lat, lng)\n[keeps last 100 points, O·1· append]
        WS-->>D: {"status": "updated", "lat": ..., "lng": ...}
    end

    D->>WS: Disconnect
    WS->>MEM: Remove from active_connections
```

---

## 🐳 Docker Architecture

```mermaid
graph TB
    subgraph Docker["🐳 Docker Compose"]
        subgraph Kafka_Stack["Kafka Stack"]
            ZK[Zookeeper :2181]
            KF[Kafka :9092]
            ZK --> KF
        end

        subgraph App["Application"]
            BE[FastAPI Backend :8001]
            RD[Redis :6379]
        end

        KF --> BE
        RD --> BE
    end

    subgraph External_Services["☁️ External Services"]
        SB[(Supabase PostgreSQL)]
        OSRM_EXT[OSRM API]
    end

    BE --> SB
    BE --> OSRM_EXT

    subgraph Deploy["🚀 Deployed"]
        RENDER[Render — Backend]
        VERCEL[Vercel — Frontend]
        VERCEL -->|HTTPS API calls| RENDER
    end
```

---

## 🛠️ Data Structures Used

| Feature | Data Structure | Why |
|---------|---------------|-----|
| Driver Assignment | **Min Heap** | O(log n) nearest driver lookup |
| Order Status | **Directed Graph** | Enforces valid state transitions |
| Surge Pricing | **Sliding Window (deque)** | O(1) add/remove, tracks last 10 mins |
| Location History | **Circular Buffer (deque maxlen)** | O(1) append, auto-evicts old data |
| Route Optimization | **TSP / Nearest Neighbor** | Finds shortest multi-stop path |
| Rating System | **Running Average** | No need to store all ratings |
| Active WebSockets | **Hash Map** | O(1) driver lookup by ID |

---

## 🚀 Getting Started

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

# Create .env
cp .env.example .env
# Fill in DATABASE_URL, SECRET_KEY, KAFKA_BOOTSTRAP_SERVERS

# Create tables
python init_db.py

# Run
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

### Docker (Full Stack)
```bash
docker-compose up --build
```

---

## 📋 API Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | ❌ | Register new user |
| POST | `/auth/login` | ❌ | Login, get JWT |
| POST | `/orders/` | ✅ | Create order |
| GET | `/orders/` | ✅ | List all orders |
| PATCH | `/orders/{id}/status` | ✅ | Update order status |
| POST | `/drivers/register` | ❌ | Register driver |
| POST | `/drivers/assign` | ❌ | Assign nearest driver |
| GET | `/drivers/` | ❌ | List all drivers |
| POST | `/ratings/` | ❌ | Rate a driver |
| GET | `/ratings/top-drivers` | ❌ | Top rated drivers |
| POST | `/routes/optimize` | ❌ | Multi-stop route |
| POST | `/routes/surge` | ❌ | Get surge multiplier |
| WS | `/drivers/ws/{id}` | ❌ | Real-time location |

Full interactive docs: `http://localhost:8001/docs`

---

## 🌐 Deployment

| Service | Platform | URL |
|---------|----------|-----|
| Backend API | Render | `https://your-app.onrender.com` |
| Frontend | Vercel | `https://your-app.vercel.app` |
| Database | Supabase | Managed PostgreSQL |

---

## 📈 Performance Characteristics

```
Driver Assignment:
  - Straight-line ranking: O(n log n) sorting → O(n) heap build
  - OSRM calls: Only top 3 candidates (not all n drivers)
  - Result: Scales to 100,000+ drivers efficiently

Surge Pricing:
  - Sliding window cleanup: O(k) where k = expired events
  - Zone lookup: O(1) hash map
  - Result: Handles thousands of concurrent zones

Route Optimization:
  - Brute force (n ≤ 8): O(n!) — max 8! = 40,320 operations
  - Nearest neighbor (n > 8): O(n²)
  - Result: Fast for real-world delivery batch sizes
```

---

## 🧪 Testing

```bash
# Health check
curl http://localhost:8001/health

# Register + login
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","name":"Test","password":"secret123"}'

# WebSocket test
python test_ws.py
```

---

## 👨‍💻 Built By

Raj Aryan — [@rajaryan](https://github.com/rajaryan)

Inspired by the engineering systems behind Swiggy, Zomato, and Uber Eats.