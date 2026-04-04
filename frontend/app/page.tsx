"use client";
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center">
      <h1 className="text-5xl font-bold mb-4">🚀 Delivery Routing System</h1>
      <p className="text-gray-400 mb-8 text-lg">
        Real-time driver assignment powered by Kafka + FastAPI
      </p>
      <div className="flex gap-4">
        <Link href="/login"
          className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold">
          Login
        </Link>
        <Link href="/dashboard"
          className="bg-gray-700 hover:bg-gray-600 px-6 py-3 rounded-lg font-semibold">
          Dashboard
        </Link>
      </div>
    </main>
  );
}