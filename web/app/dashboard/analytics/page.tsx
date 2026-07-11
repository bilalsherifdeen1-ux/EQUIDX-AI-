"use client";

import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import DashboardShell from "../../components/DashboardShell";
import { api } from "@/lib/api-client";

interface Overview {
  total_patients: number;
  total_samples: number;
  total_reports: number;
  analysis_completion_rate: number;
  samples_by_status: Record<string, number>;
  samples_by_type: Record<string, number>;
}

export default function AnalyticsPage() {
  const [overview, setOverview] = useState<Overview | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("equidx_access_token") ?? undefined : undefined;
    api
      .get<Overview>("/api/v1/analytics/overview", token)
      .then(setOverview)
      .catch(() => setErrorMsg("Analytics service unavailable — start the `analytics` container and sign in."));
  }, []);

  const typeData = overview
    ? Object.entries(overview.samples_by_type).map(([type, count]) => ({ type: type.replace("_", " "), count }))
    : [];

  return (
    <DashboardShell>
      <h1 className="font-display text-2xl text-mist-100">Analytics</h1>
      <p className="mt-1 text-sm text-mist-500">Platform-wide rollups from the analytics microservice.</p>

      {errorMsg && <p className="mt-6 text-sm text-amber-400">{errorMsg}</p>}

      {overview && (
        <>
          <div className="mt-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
            <div className="rounded-xl border border-ink-700 p-5">
              <p className="text-xs text-mist-500">Patients</p>
              <p className="mt-2 font-mono text-2xl text-signal-400">{overview.total_patients}</p>
            </div>
            <div className="rounded-xl border border-ink-700 p-5">
              <p className="text-xs text-mist-500">Samples</p>
              <p className="mt-2 font-mono text-2xl text-signal-400">{overview.total_samples}</p>
            </div>
            <div className="rounded-xl border border-ink-700 p-5">
              <p className="text-xs text-mist-500">Reports</p>
              <p className="mt-2 font-mono text-2xl text-signal-400">{overview.total_reports}</p>
            </div>
            <div className="rounded-xl border border-ink-700 p-5">
              <p className="text-xs text-mist-500">Completion rate</p>
              <p className="mt-2 font-mono text-2xl text-signal-400">
                {(overview.analysis_completion_rate * 100).toFixed(0)}%
              </p>
            </div>
          </div>

          <div className="mt-8 rounded-xl border border-ink-700 p-6" style={{ height: 320 }}>
            <h2 className="font-display text-lg text-mist-100">Samples by domain</h2>
            <ResponsiveContainer width="100%" height="85%">
              <BarChart data={typeData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#182622" />
                <XAxis dataKey="type" stroke="#7E9691" fontSize={12} />
                <YAxis stroke="#7E9691" fontSize={12} />
                <Tooltip contentStyle={{ background: "#0B1210", border: "1px solid #22332E" }} />
                <Bar dataKey="count" fill="#3DDC97" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </DashboardShell>
  );
}
