"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { auth } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [isRegister, setIsRegister] = useState(false);
  const [form, setForm]   = useState({ email: "", name: "", password: "" });
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    try {
      const res = isRegister
        ? await auth.register({ ...form, role: "customer" })
        : await auth.login({ email: form.email, password: form.password });

      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("user",  JSON.stringify(res.data.user));
      router.push("/dashboard");
    } catch (e: any) {
      setError(e.response?.data?.detail || "Something went wrong");
    }
  };

  return (
    <main className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="bg-gray-900 p-8 rounded-xl w-96 shadow-xl">
        <h2 className="text-2xl font-bold text-white mb-6">
          {isRegister ? "Create Account" : "Login"}
        </h2>

        {isRegister && (
          <input
            className="w-full bg-gray-800 text-white p-3 rounded-lg mb-3"
            placeholder="Full Name"
            value={form.name}
            onChange={e => setForm({ ...form, name: e.target.value })}
          />
        )}
        <input
          className="w-full bg-gray-800 text-white p-3 rounded-lg mb-3"
          placeholder="Email"
          type="email"
          value={form.email}
          onChange={e => setForm({ ...form, email: e.target.value })}
        />
        <input
          className="w-full bg-gray-800 text-white p-3 rounded-lg mb-4"
          placeholder="Password"
          type="password"
          value={form.password}
          onChange={e => setForm({ ...form, password: e.target.value })}
        />

        {error && <p className="text-red-400 mb-3 text-sm">{error}</p>}

        <button
          onClick={handleSubmit}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold"
        >
          {isRegister ? "Register" : "Login"}
        </button>

        <p className="text-gray-400 text-sm mt-4 text-center">
          {isRegister ? "Already have an account?" : "New here?"}{" "}
          <button
            onClick={() => setIsRegister(!isRegister)}
            className="text-blue-400 hover:underline"
          >
            {isRegister ? "Login" : "Register"}
          </button>
        </p>
      </div>
    </main>
  );
}