"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api-client";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ full_name: "", email: "", password: "", role: "researcher" });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await api.post("/api/v1/auth/register", form);
      router.push("/login");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-ink-900 px-6">
      <div className="w-full max-w-sm">
        <Link href="/" className="font-display text-lg font-semibold text-mist-100">
          EQUIDX <span className="text-signal-500">AI</span>
        </Link>
        <h1 className="mt-8 font-display text-2xl text-mist-100">Request research access</h1>
        <p className="mt-1 text-sm text-mist-500">Creates a demo account against synthetic data only.</p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-4">
          <div>
            <label className="mb-1 block text-xs text-mist-500">Full name</label>
            <input
              required value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })}
              className="w-full rounded-lg border border-ink-600 bg-ink-950 px-3 py-2 text-sm text-mist-100 outline-none focus:border-signal-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs text-mist-500">Email</label>
            <input
              type="email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full rounded-lg border border-ink-600 bg-ink-950 px-3 py-2 text-sm text-mist-100 outline-none focus:border-signal-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs text-mist-500">Password</label>
            <input
              type="password" required minLength={8} value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="w-full rounded-lg border border-ink-600 bg-ink-950 px-3 py-2 text-sm text-mist-100 outline-none focus:border-signal-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs text-mist-500">Role</label>
            <select
              value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}
              className="w-full rounded-lg border border-ink-600 bg-ink-950 px-3 py-2 text-sm text-mist-100 outline-none focus:border-signal-500"
            >
              <option value="researcher">Researcher</option>
              <option value="clinician">Clinician</option>
              <option value="lab_tech">Lab technician</option>
            </select>
          </div>
          {error && <p className="text-sm text-red-400">{error}</p>}
          <button
            type="submit" disabled={loading}
            className="w-full rounded-full bg-signal-500 px-4 py-2.5 text-sm font-medium text-ink-950 hover:bg-signal-400 disabled:opacity-50"
          >
            {loading ? "Creating account…" : "Create account"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-mist-500">
          Already have access?{" "}
          <Link href="/login" className="trace-underline text-signal-400">Sign in</Link>
        </p>
      </div>
    </main>
  );
}
