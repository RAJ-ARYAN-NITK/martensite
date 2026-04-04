"use client";
import { useEffect, useState } from "react";
import dynamic from "next/dynamic";

// Leaflet must be dynamically imported (no SSR)
const MapContainer  = dynamic(() => import("react-leaflet").then(m => m.MapContainer),  { ssr: false });
const TileLayer     = dynamic(() => import("react-leaflet").then(m => m.TileLayer),     { ssr: false });
const Marker        = dynamic(() => import("react-leaflet").then(m => m.Marker),        { ssr: false });
const Popup         = dynamic(() => import("react-leaflet").then(m => m.Popup),         { ssr: false });

interface Driver {
  driver_id: string;
  name: string;
  status: string;
  current_location: { lat: number; lng: number };
}

export default function Map({ drivers }: { drivers: Driver[] }) {
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);
  if (!mounted) return <div className="h-96 bg-gray-800 rounded-xl animate-pulse" />;

  return (
    <div className="h-96 rounded-xl overflow-hidden">
      <MapContainer
        center={[12.9716, 77.5946]}
        zoom={13}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="© OpenStreetMap"
        />
        {drivers.map((driver) => (
          <Marker
            key={driver.driver_id}
            position={[
              driver.current_location.lat,
              driver.current_location.lng,
            ]}
          >
            <Popup>
              <strong>{driver.name}</strong>
              <br />
              Status: {driver.status}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}