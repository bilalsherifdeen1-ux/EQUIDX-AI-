"use client";

import { useEffect, useState } from "react";
import DashboardShell from "../components/DashboardShell";
import { api } from "@/lib/api-client";

interface UserRow { id: string; email: string; full_name: string; role: string; is_active: boolean; }
interface AuditRow { id: string; action: string; resource_type: string; resource_id: string; created_at: string; }

export default function AdminPage() {
  const [users, setUsers] = useState<UserRow[]>([]);
  const [logs, setLogs] = useState<AuditRow[]>([]);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("equidx_access_token") ?? undefined : undefined;
    Promise.all([
      api.get<UserRow[]>("/api/v1/admin/users", token),
      api.get<AuditRow[]>("/api/v1/admin/audit-logs", token),
    ])
      .then(([u, l]) => { setUsers(u); setLogs(l); })
      .catch(() => setErrorMsg("Admin role required. Sign in as admin@equidx.ai."));
  }, []);

  return (
    <DashboardShell>
      <h1 className="font-display text-2xl text-mist-100">Admin Portal</h1>
      <p className="mt-1 text-sm text-mist-500">User management and audit trail — ADMIN role only.</p>

      {errorMsg && <p className="mt-6 text-sm text-amber-400">{errorMsg}</p>}

      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-ink-700 p-5">
          <h2 className="font-display text-lg text-mist-100">Users</h2>
          <ul className="mt-4 space-y-2 text-sm">
            {users.map((u) => (
              <li key={u.id} className="flex items-center justify-between border-b border-ink-700 py-2">
                <span className="text-mist-100">{u.full_name} <span className="text-mist-500">({u.email})</span></span>
                <span className="font-mono text-xs uppercase text-signal-400">{u.role}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="rounded-xl border border-ink-700 p-5">
          <h2 className="font-display text-lg text-mist-100">Recent audit log</h2>
          <ul className="mt-4 space-y-2 text-sm">
            {logs.map((l) => (
              <li key={l.id} className="border-b border-ink-700 py-2 text-mist-300">
                <span className="font-mono text-signal-400">{l.action}</span> on {l.resource_type} · {new Date(l.created_at).toLocaleString()}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </DashboardShell>
  );
}
