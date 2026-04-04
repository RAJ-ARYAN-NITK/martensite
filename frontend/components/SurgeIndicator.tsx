"use client";

export default function SurgeIndicator({ surge }: { surge: number }) {
  const color = surge >= 2    ? "text-red-400"
              : surge >= 1.5  ? "text-orange-400"
              : surge > 1     ? "text-yellow-400"
              :                 "text-green-400";

  return (
    <div className="bg-gray-900 rounded-xl p-6 text-center">
      <h2 className="text-xl font-bold text-white mb-2">⚡ Surge Pricing</h2>
      <p className={`text-5xl font-bold ${color}`}>{surge}x</p>
      <p className="text-gray-400 mt-2 text-sm">
        {surge === 1 ? "Normal pricing" : `High demand — ${surge}x multiplier active`}
      </p>
    </div>
  );
}