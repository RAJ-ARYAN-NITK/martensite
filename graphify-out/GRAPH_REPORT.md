# Graph Report - /Users/rajaryan/Martensite  (2026-05-14)

## Corpus Check
- Corpus is ~13,169 words - fits in a single context window. You may not need a graph.

## Summary
- 249 nodes · 313 edges · 30 communities (24 shown, 6 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 50 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_System Architecture & Tech Stack|System Architecture & Tech Stack]]
- [[_COMMUNITY_Driver Models & Schemas|Driver Models & Schemas]]
- [[_COMMUNITY_Authentication & Users|Authentication & Users]]
- [[_COMMUNITY_Order Processing & Events|Order Processing & Events]]
- [[_COMMUNITY_Frontend Components|Frontend Components]]
- [[_COMMUNITY_Driver Ratings|Driver Ratings]]
- [[_COMMUNITY_Route & Driver Assignment|Route & Driver Assignment]]
- [[_COMMUNITY_App Startup & Consumers|App Startup & Consumers]]
- [[_COMMUNITY_Surge Pricing|Surge Pricing]]
- [[_COMMUNITY_Driver Store|Driver Store]]
- [[_COMMUNITY_Location History|Location History]]
- [[_COMMUNITY_Driver Management APIs|Driver Management APIs]]
- [[_COMMUNITY_Map Components|Map Components]]
- [[_COMMUNITY_App Layout|App Layout]]
- [[_COMMUNITY_Kafka Topics|Kafka Topics]]
- [[_COMMUNITY_Next.js Branding|Next.js Branding]]
- [[_COMMUNITY_ESLint Config|ESLint Config]]
- [[_COMMUNITY_Next.js Config|Next.js Config]]
- [[_COMMUNITY_PostCSS Config|PostCSS Config]]
- [[_COMMUNITY_Vercel Logo|Vercel Logo]]

## God Nodes (most connected - your core abstractions)
1. `Delivery Routing System` - 18 edges
2. `_to_schema()` - 10 edges
3. `SurgeCalculator` - 8 edges
4. `DriverLocationHistory` - 7 edges
5. `get_straight_line_km()` - 7 edges
6. `find_nearest_driver()` - 7 edges
7. `_get_db()` - 7 edges
8. `Location` - 6 edges
9. `update_order_status()` - 6 edges
10. `register()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Redis` --conceptually_related_to--> `WebSockets`  [INFERRED]
  docker-compose.yml → README.md
- `Frontend Application` --implements--> `Next.js Framework`  [INFERRED]
  frontend/public/next.svg → frontend/AGENTS.md
- `register_driver()` --calls--> `DriverSchema`  [INFERRED]
  backend/routers/drivers.py → backend/models/driver.py
- `update_status()` --calls--> `update_order_status()`  [INFERRED]
  backend/routers/orders.py → backend/services/order_service.py
- `get_orders_by_status()` --calls--> `OrderStatus`  [INFERRED]
  backend/routers/orders.py → backend/models/order.py

## Hyperedges (group relationships)
- **Core Tech Stack** — readme_tech_stack_fastapi, readme_tech_stack_kafka, readme_tech_stack_supabase, readme_tech_stack_sqlalchemy, readme_tech_stack_websockets, readme_tech_stack_jwt [EXTRACTED 1.00]
- **Kafka Event Topics** — readme_kafka_topics, readme_new_orders_topic, readme_driver_assignments_topic, readme_order_status_updates_topic [EXTRACTED 1.00]
- **Core Algorithms** — readme_min_heap_driver_assignment, readme_sliding_window_surge_pricing, readme_directed_graph_state_machine, readme_tsp_route_optimization, readme_running_average_ratings, readme_circular_buffer_location [EXTRACTED 1.00]
- **Next.js Branding Assets** — next_svg, nextjs_framework [EXTRACTED 1.00]

## Communities (30 total, 6 thin omitted)

### Community 0 - "System Architecture & Tech Stack"
Cohesion: 0.11
Nodes (26): Python Dependencies, FastAPI Backend, Kafka, Redis, Docker Compose Services, Zookeeper, Next.js, Circular Buffer Location History (+18 more)

### Community 1 - "Driver Models & Schemas"
Cohesion: 0.12
Nodes (17): BaseModel, Enum, AssignDriverRequest, AssignmentResult, DriverSchema, DriverStatus, Location, RegisterDriverRequest (+9 more)

### Community 2 - "Authentication & Users"
Cohesion: 0.11
Nodes (18): Base, get_current_user(), Driver, Config, TokenResponse, User, UserLogin, UserRegister (+10 more)

### Community 3 - "Order Processing & Events"
Cohesion: 0.12
Nodes (16): Order, OrderStatus, create_order(), get_orders_by_status(), update_status(), get_producer(), publish_driver_assignment(), publish_new_order() (+8 more)

### Community 4 - "Frontend Components"
Cohesion: 0.12
Nodes (9): STATUS_COLORS, STATUS_COLORS, Map, API, auth, drivers, orders, routes (+1 more)

### Community 5 - "Driver Ratings"
Cohesion: 0.12
Nodes (16): RatingRequest, submit_rating(), top_drivers(), build_driver_heap(), get_top_drivers(), increment_trip_count(), pop_nearest(), rate_driver() (+8 more)

### Community 6 - "Route & Driver Assignment"
Cohesion: 0.17
Nodes (14): optimize_route(), assign_driver(), find_nearest_driver(), Uses Min Heap for O(log n) nearest driver lookup.     Also factors in driver rat, get_driving_info(), get_straight_line_km(), Haversine straight-line distance in km., Returns (distance_km, duration_mins) via OSRM.     Falls back to (None, None) on (+6 more)

### Community 7 - "App Startup & Consumers"
Cohesion: 0.17
Nodes (7): startup_event(), process_order(), Auto-assign nearest driver when a new order arrives., Runs in a background thread — consumes new-orders topic., Start consumer in background so it doesn't block FastAPI., start_consumer_thread(), start_order_consumer()

### Community 8 - "Surge Pricing"
Cohesion: 0.22
Nodes (6): Round to 2 decimals → ~1.1km grid zones., Remove events outside the sliding window., Record a new order in this zone., Surge = demand / supply ratio in sliding window.         Returns multiplier: 1.0, Sliding window — tracks orders in last 10 mins per zone.     Zone = rounded lat/, SurgeCalculator

### Community 9 - "Driver Store"
Cohesion: 0.47
Nodes (9): add_driver(), get_all_drivers(), get_available_drivers(), _get_db(), get_driver(), Convert SQLAlchemy ORM object → Pydantic schema., _to_schema(), update_driver_location() (+1 more)

### Community 12 - "Map Components"
Cohesion: 0.29
Nodes (5): Driver, MapContainer, Marker, Popup, TileLayer

### Community 13 - "App Layout"
Cohesion: 0.4
Nodes (3): geistMono, geistSans, metadata

### Community 15 - "Kafka Topics"
Cohesion: 0.83
Nodes (4): driver-assignments topic, Kafka Topics, new-orders topic, order-status-updates topic

### Community 16 - "Next.js Branding"
Cohesion: 1.0
Nodes (3): Frontend Application, Next.js Logo SVG, Next.js Framework

## Knowledge Gaps
- **50 isolated node(s):** `config`, `eslintConfig`, `nextConfig`, `geistSans`, `geistMono` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Location` connect `Driver Models & Schemas` to `Driver Store`, `App Startup & Consumers`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `AssignmentResult` connect `Driver Models & Schemas` to `Route & Driver Assignment`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `process_order()` connect `App Startup & Consumers` to `Driver Models & Schemas`, `Order Processing & Events`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `_to_schema()` (e.g. with `DriverSchema` and `Location`) actually correct?**
  _`_to_schema()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `config`, `eslintConfig`, `nextConfig` to the rest of the system?**
  _50 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `System Architecture & Tech Stack` be split into smaller, more focused modules?**
  _Cohesion score 0.11 - nodes in this community are weakly interconnected._
- **Should `Driver Models & Schemas` be split into smaller, more focused modules?**
  _Cohesion score 0.12 - nodes in this community are weakly interconnected._