"use client";

const STATUS_COLORS: Record<string, string> = {
  pending:    "bg-yellow-500",
  assigned:   "bg-blue-500",
  picked_up:  "bg-purple-500",
  in_transit: "bg-orange-500",
  delivered:  "bg-green-500",
};

export default function OrderBoard({ orders }: { orders: any[] }) {
  return (
    <div className="bg-gray-900 rounded-xl p-6">
      <h2 className="text-xl font-bold text-white mb-4">📦 Live Orders</h2>
      {orders.length === 0 ? (
        <p className="text-gray-400">No orders yet</p>
      ) : (
        <div className="space-y-3">
          {orders.map((order) => (
            <div key={order.id} className="bg-gray-800 rounded-lg p-4 flex justify-between items-center">
              <div>
                <p className="text-white font-mono text-sm">{order.id.slice(0, 8)}...</p>
                <p className="text-gray-400 text-xs mt-1">
                  Customer: {order.customer_id}
                </p>
                <p className="text-gray-400 text-xs">
                  ₹{order.final_price}
                  {order.surge_multiplier > 1 && (
                    <span className="text-orange-400 ml-2">
                      🔥 {order.surge_multiplier}x surge
                    </span>
                  )}
                </p>
              </div>
              <span className={`${STATUS_COLORS[order.status] || "bg-gray-500"} text-white text-xs px-3 py-1 rounded-full`}>
                {order.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}