"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { drivers as driversApi, orders as ordersApi, routes } from "@/lib/api";
import dynamic from "next/dynamic";
import OrderBoard from "@/components/OrderBoard";
import DriverList from "@/components/DriverList";
import SurgeIndicator from "@/components/SurgeIndicator";

const Map = dynamic(() => import("@/components/Map"), { ssr: false });

export default function Dashboard() {
  const router = useRouter();
  const [driversList, setDriversList]  = useState([]);
  const [ordersList,  setOrdersList]   = useState([]);
  const [surge,       setSurge]        = useState(1.0);
  const [loading,     setLoading]      = useState(true);

  const fetchAll = async () => {
    try {
      const [driversRes, ordersRes, surgeRes] = await Promise.all([
        driversApi.list(),
        ordersApi.list(),
        routes.surge({ lat: 12.9716, lng: 77.5946, available_drivers: 2 }),
      ]);
      setDriversList(driversRes.data.drivers || []);
      setOrdersList(ordersRes.data);
      setSurge(surgeRes.data.surge_multiplier);
    } catch (e: any) {
      if (e.response?.status === 401) router.push("/login");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) { router.push("/login"); return; }
    fetchAll();
    // Auto-refresh every 10 seconds
    const interval = setInterval(fetchAll, 10000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <p className="text-white text-xl">Loading dashboard...</p>
    </div>
  );

  return (
    <main className="min-h-screen bg-gray-950 text-white p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">🚀 Delivery Dashboard</h1>
        <div className="flex gap-3">
          <button
            onClick={fetchAll}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-sm"
          >
            Refresh
          </button>
          <button
            onClick={() => { localStorage.clear(); router.push("/login"); }}
            className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg text-sm"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-900 rounded-xl p-5 text-center">
          <p className="text-4xl font-bold text-blue-400">{driversList.length}</p>
          <p className="text-gray-400 mt-1">Total Drivers</p>
        </div>
        <div className="bg-gray-900 rounded-xl p-5 text-center">
          <p className="text-4xl font-bold text-green-400">
            {driversList.filter((d: any) => d.status === "available").length}
          </p>
          <p className="text-gray-400 mt-1">Available</p>
        </div>
        <div className="bg-gray-900 rounded-xl p-5 text-center">
          <p className="text-4xl font-bold text-yellow-400">{ordersList.length}</p>
          <p className="text-gray-400 mt-1">Total Orders</p>
        </div>
      </div>

      {/* Map */}
      <div className="mb-6">
        <Map drivers={driversList} />
      </div>

      {/* Bottom Grid */}
      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2">
          <OrderBoard orders={ordersList} />
        </div>
        <div className="space-y-4">
          <SurgeIndicator surge={surge} />
          <DriverList drivers={driversList} />
        </div>
      </div>
    </main>
  );
}