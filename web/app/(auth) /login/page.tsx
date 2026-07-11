"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { login } from "@/lib/api-client";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const tokens = await login(email, password);
      localStorage.setItem("equidx_access_token", tokens.access_token);
      localStorage.setItem("equidx_refresh_token", tokens.refresh_token);
      router.push("/dashboard");
    } catch {
      setError("Invalid email or password.");
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
        <h1 className="mt-8 font-display text-2xl text-mist-100">Sign in</h1>
        <p className="mt-1 text-sm text-mist-500">Research/clinician access — demo credentials only.</p>

        <form onSubmit={handleSubmit} className="mt-8 space-y-4">
          <div>
            <label className="mb-1 block text-xs text-mist-500">Email</label>
            <input
              type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg border border-ink-600 bg-ink-950 px-3 py-2 text-sm text-mist-100 outline-none focus:border-signal-500"
              placeholder="you@equidx.ai"
            />
          </div>
          <div>
            <label className="mb-1 block text-xs text-mist-500">Password</label>
            <input
              type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg border border-ink-600 bg-ink-950 px-3 py-2 text-sm text-mist-100 outline-none focus:border-signal-500"
              placeholder="••••••••"
            />
          </div>
          {error && <p className="text-sm text-red-400">{error}</p>}
          <button
            type="submit" disabled={loading}
            className="w-full rounded-full bg-signal-500 px-4 py-2.5 text-sm font-medium text-ink-950 hover:bg-signal-400 disabled:opacity-50"
          >
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-mist-500">
          No account?{" "}
          <Link href="/register" className="trace-underline text-signal-400">Request access</Link>
        </p>
      </div>
    </main>
  );
}
