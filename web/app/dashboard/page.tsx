import DashboardShell from "../components/DashboardShell";

const stats = [
  { label: "Synthetic patients", value: "25" },
  { label: "Samples tracked", value: "58" },
  { label: "Reports generated", value: "41" },
  { label: "Avg. confidence", value: "0.86" },
];

export default function DashboardOverview() {
  return (
    <DashboardShell>
      <h1 className="font-display text-2xl text-mist-100">Overview</h1>
      <p className="mt-1 text-sm text-mist-500">
        All figures below reflect synthetic demo data seeded for this
        environment.
      </p>

      <div className="mt-8 grid grid-cols-2 gap-4 lg:grid-cols-4">
        {stats.map((s) => (
          <div key={s.label} className="rounded-xl border border-ink-700 p-5">
            <p className="text-xs text-mist-500">{s.label}</p>
            <p className="mt-2 font-mono text-2xl text-signal-400">{s.value}</p>
          </div>
        ))}
      </div>

      <div className="mt-8 rounded-xl border border-ink-700 p-6">
        <h2 className="font-display text-lg text-mist-100">Getting started</h2>
        <ol className="mt-4 space-y-2 text-sm text-mist-300">
          <li>1. Register a synthetic patient under <span className="text-signal-400">Patients</span>.</li>
          <li>2. Register a sample against that patient under <span className="text-signal-400">Samples</span>.</li>
          <li>3. Generate a placeholder AI report under <span className="text-signal-400">Reports</span>.</li>
          <li>4. Review platform-wide trends under <span className="text-signal-400">Analytics</span>.</li>
        </ol>
      </div>
    </DashboardShell>
  );
}
