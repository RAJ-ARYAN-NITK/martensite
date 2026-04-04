"use client";

const STATUS_COLORS: Record<string, string> = {
  available: "text-green-400",
  on_trip:   "text-yellow-400",
  offline:   "text-red-400",
};

export default function DriverList({ drivers }: { drivers: any[] }) {
  return (
    <div className="bg-gray-900 rounded-xl p-6">
      <h2 className="text-xl font-bold text-white mb-4">🚗 Drivers</h2>
      {drivers.map((driver) => (
        <div key={driver.driver_id} className="bg-gray-800 rounded-lg p-4 mb-3 flex justify-between items-center">
          <div>
            <p className="text-white font-semibold">{driver.name}</p>
            <p className="text-gray-400 text-xs">{driver.vehicle_type}</p>
            <p className="text-yellow-400 text-xs">⭐ {driver.rating}</p>
          </div>
          <span className={`${STATUS_COLORS[driver.status]} text-sm font-semibold`}>
            {driver.status}
          </span>
        </div>
      ))}
    </div>
  );
}