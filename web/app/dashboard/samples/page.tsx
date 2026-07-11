"use client";

import { useEffect, useState } from "react";
import DashboardShell from "../../components/DashboardShell";
import { api } from "@/lib/api-client";

interface Sample {
  id: string;
  barcode: string;
  sample_type: string;
  status: string;
  created_at: string;
}

const statusColor: Record<string, string> = {
  registered: "text-mist-300", collected: "text-signal-400", in_transit: "text-amber-400",
  received: "text-signal-400", processing: "text-amber-400", analyzed: "text-signal-500", rejected: "text-red-400",
};

export default function SamplesPage() {
  const [samples, setSamples] = useState<Sample[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("equidx_access_token") ?? undefined : undefined;
    api
      .get<Sample[]>("/api/v1/samples", token)
      .then(setSamples)
      .catch(() => setErrorMsg("Could not load samples. Sign in and ensure the backend is running."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <DashboardShell>
      <h1 className="font-display text-2xl text-mist-100">Samples</h1>
      <p className="mt-1 text-sm text-mist-500">Tracked biosensor / lab samples across all synthetic patients.</p>

      <div className="mt-6 overflow-hidden rounded-xl border border-ink-700">
        <table className="w-full text-left text-sm">
          <thead className="bg-ink-800 text-xs uppercase text-mist-500">
            <tr>
              <th className="px-4 py-3">Barcode</th>
              <th className="px-4 py-3">Type</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Registered</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-ink-700">
            {samples.map((s) => (
              <tr key={s.id} className="hover:bg-ink-800/50">
                <td className="px-4 py-3 font-mono text-signal-400">{s.barcode}</td>
                <td className="px-4 py-3 text-mist-100 capitalize">{s.sample_type.replace("_", " ")}</td>
                <td className={`px-4 py-3 capitalize ${statusColor[s.status] ?? "text-mist-300"}`}>{s.status.replace("_", " ")}</td>
                <td className="px-4 py-3 text-mist-500">{new Date(s.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {loading && <p className="p-6 text-center text-sm text-mist-500">Loading…</p>}
        {!loading && errorMsg && <p className="p-6 text-center text-sm text-amber-400">{errorMsg}</p>}
      </div>
    </DashboardShell>
  );
}
