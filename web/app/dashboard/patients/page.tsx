"use client";

import { useEffect, useState } from "react";
import DashboardShell from "../../components/DashboardShell";
import { api } from "@/lib/api-client";

interface Patient {
  id: string;
  mrn: string;
  first_name: string;
  last_name: string;
  sex: string;
  is_synthetic: boolean;
}

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("equidx_access_token") ?? undefined : undefined;
    api
      .get<Patient[]>("/api/v1/patients", token)
      .then(setPatients)
      .catch(() => setErrorMsg("Could not load patients. Sign in and ensure the backend is running."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <DashboardShell>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-2xl text-mist-100">Patients</h1>
          <p className="mt-1 text-sm text-mist-500">Synthetic patient records only — see banner disclaimer.</p>
        </div>
      </div>

      <div className="mt-6 overflow-hidden rounded-xl border border-ink-700">
        <table className="w-full text-left text-sm">
          <thead className="bg-ink-800 text-xs uppercase text-mist-500">
            <tr>
              <th className="px-4 py-3">MRN</th>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Sex</th>
              <th className="px-4 py-3">Synthetic</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-ink-700">
            {patients.map((p) => (
              <tr key={p.id} className="hover:bg-ink-800/50">
                <td className="px-4 py-3 font-mono text-signal-400">{p.mrn}</td>
                <td className="px-4 py-3 text-mist-100">{p.first_name} {p.last_name}</td>
                <td className="px-4 py-3 text-mist-300 capitalize">{p.sex}</td>
                <td className="px-4 py-3 text-mist-300">{p.is_synthetic ? "Yes" : "No"}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {loading && <p className="p-6 text-center text-sm text-mist-500">Loading…</p>}
        {!loading && errorMsg && <p className="p-6 text-center text-sm text-amber-400">{errorMsg}</p>}
        {!loading && !errorMsg && patients.length === 0 && (
          <p className="p-6 text-center text-sm text-mist-500">No patients yet — run the seed script.</p>
        )}
      </div>
    </DashboardShell>
  );
}
