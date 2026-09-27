import Link from "next/link";
import NavBar from "./components/NavBar";
import DisclaimerBanner from "./components/DisclaimerBanner";

const capabilities = [
  {
    number: "01",
    title: "Signal to sample",
    body: "A biosensor-oriented data path that keeps collection, barcode identity, status transitions, and provenance visible from the first event.",
  },
  {
    number: "02",
    title: "Evidence before inference",
    body: "A modular AI boundary for feature extraction, model calls, confidence, and report assembly—so each stage can be tested independently.",
  },
  {
    number: "03",
    title: "Operational by design",
    body: "Service health, audit trails, role-aware access, analytics, and a deployment shape that can grow from a research sandbox into a controlled system.",
  },
];

export default function HomePage() {
  return (
    <main className="min-h-screen bg-ink-900">
      <DisclaimerBanner />
      <NavBar />

      <section className="relative overflow-hidden border-b border-ink-700 bg-trace-grid">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_75%_20%,rgba(61,220,151,0.14),transparent_32%)]" />
        <div className="relative mx-auto grid max-w-6xl gap-16 px-6 pb-24 pt-16 lg:grid-cols-[1.1fr_0.9fr] lg:items-end lg:pt-24">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-signal-400">Research platform / biosensor AI</p>
            <h1 className="mt-6 max-w-4xl font-display text-5xl font-semibold tracking-tight text-mist-100 sm:text-7xl">
              From raw signal to <span className="text-signal-400">auditable insight.</span>
            </h1>
            <p className="mt-7 max-w-2xl text-lg leading-8 text-mist-300">
              EquiDx AI is a modular research prototype for exploring how biosensor data, clinical workflows, and interpretable machine learning can share one reliable engineering surface.
            </p>
            <div className="mt-9 flex flex-wrap gap-3">
              <Link href="/engineering/equidx-ai" className="rounded-full bg-signal-500 px-5 py-3 text-sm font-medium text-ink-950 hover:bg-signal-400">
                Read the engineering write-up ↗
              </Link>
              <Link href="/disclaimer" className="rounded-full border border-ink-600 px-5 py-3 text-sm text-mist-100 hover:border-signal-500 hover:text-signal-400">
                Research boundaries
              </Link>
            </div>
          </div>
          <div className="rounded-2xl border border-signal-500/30 bg-ink-950/80 p-6 shadow-2xl shadow-signal-500/5">
            <div className="flex items-center justify-between border-b border-ink-700 pb-4">
              <span className="font-mono text-xs uppercase tracking-widest text-mist-500">Pipeline status</span>
              <span className="flex items-center gap-2 font-mono text-xs text-signal-400"><span className="h-2 w-2 rounded-full bg-signal-400" /> synthetic environment</span>
            </div>
            <div className="mt-6 space-y-5 font-mono text-sm">
              {[
                ["biosensor input", "captured"],
                ["sample identity", "verified"],
                ["feature boundary", "versioned"],
                ["report output", "review required"],
              ].map(([label, state], index) => (
                <div key={label} className="flex items-center gap-4">
                  <span className="text-mist-500">0{index + 1}</span>
                  <div className="h-px flex-1 bg-ink-700"><div className="h-px w-2/3 bg-signal-500/70" /></div>
                  <span className="text-mist-300">{label}</span>
                  <span className="text-signal-400">{state}</span>
                </div>
              ))}
            </div>
            <p className="mt-7 border-t border-ink-700 pt-4 text-xs leading-5 text-mist-500">A transparent research workflow is more useful than an impressive black box. Every output stays inside its stated boundary.</p>
          </div>
        </div>
      </section>

      <section id="platform" className="mx-auto max-w-6xl px-6 py-24">
        <div className="flex flex-col justify-between gap-5 border-b border-ink-700 pb-8 md:flex-row md:items-end">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-signal-400">The platform</p>
            <h2 className="mt-3 font-display text-4xl text-mist-100">A system for the full path.</h2>
          </div>
          <p className="max-w-md text-sm leading-6 text-mist-500">The interesting problem is not only model accuracy. It is keeping identity, state, inference, review, and evidence connected as the system changes.</p>
        </div>
        <div className="mt-8 grid gap-4 md:grid-cols-3">
          {capabilities.map((item) => (
            <article key={item.number} className="rounded-2xl border border-ink-700 bg-ink-800/50 p-6 transition hover:-translate-y-1 hover:border-signal-500/50">
              <span className="font-mono text-xs text-signal-400">{item.number} / capability</span>
              <h3 className="mt-12 font-display text-2xl text-mist-100">{item.title}</h3>
              <p className="mt-4 text-sm leading-6 text-mist-500">{item.body}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="pipeline" className="border-y border-ink-700 bg-ink-950/60">
        <div className="mx-auto grid max-w-6xl gap-12 px-6 py-24 lg:grid-cols-[0.8fr_1.2fr]">
          <div>
            <p className="font-mono text-xs uppercase tracking-[0.28em] text-signal-400">The engineering thesis</p>
            <h2 className="mt-3 font-display text-4xl text-mist-100">Make the pipeline legible.</h2>
            <p className="mt-6 text-sm leading-7 text-mist-300">EquiDx is shaped as a set of boundaries rather than a single prediction endpoint. That makes it easier to test failure modes, preserve provenance, and explain which part of the system produced a result.</p>
            <Link href="/engineering/equidx-ai" className="mt-8 inline-block text-sm text-signal-400 trace-underline">See architecture, trade-offs, and next steps ↗</Link>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {["Input contracts", "Sample identity", "Feature versioning", "Model boundary", "Confidence + limits", "Human review"].map((label, index) => (
              <div key={label} className="flex items-center gap-4 rounded-xl border border-ink-700 px-5 py-4">
                <span className="font-mono text-xs text-mist-500">0{index + 1}</span>
                <span className="text-sm text-mist-100">{label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="mx-auto flex max-w-6xl flex-col gap-4 px-6 py-10 text-xs text-mist-500 sm:flex-row sm:items-center sm:justify-between">
        <span className="font-mono uppercase tracking-widest">EquiDx AI / research prototype</span>
        <span>Synthetic data only · not for clinical use</span>
      </footer>
    </main>
  );
}
