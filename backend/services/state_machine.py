import networkx as nx
from models.order import OrderStatus

# Build directed graph of valid state transitions
# Each edge = a valid transition
_graph = nx.DiGraph()
_graph.add_edges_from([
    (OrderStatus.PENDING,    OrderStatus.ASSIGNED),
    (OrderStatus.ASSIGNED,   OrderStatus.PICKED_UP),
    (OrderStatus.PICKED_UP,  OrderStatus.IN_TRANSIT),
    (OrderStatus.IN_TRANSIT, OrderStatus.DELIVERED),
    # Cancellation allowed from any non-terminal state
    (OrderStatus.PENDING,    "cancelled"),
    (OrderStatus.ASSIGNED,   "cancelled"),
    (OrderStatus.PICKED_UP,  "cancelled"),
])


def is_valid_transition(current: OrderStatus, new_status: str) -> bool:
    """O(1) edge lookup in directed graph."""
    try:
        new_enum = OrderStatus(new_status)
        return _graph.has_edge(current, new_enum)
    except ValueError:
        # Check cancellation
        return _graph.has_edge(current, new_status)


def get_allowed_transitions(current: OrderStatus) -> list[str]:
    """Get all valid next states from current."""
    return [
        str(n.value) if hasattr(n, 'value') else str(n)
        for n in _graph.successors(current)
    ]


def get_full_path(from_status: OrderStatus, to_status: OrderStatus) -> list:
    """Find shortest path between two statuses."""
    try:
        path = nx.shortest_path(_graph, from_status, to_status)
        return [s.value if hasattr(s, 'value') else s for s in path]
    except nx.NetworkXNoPath:
        return []