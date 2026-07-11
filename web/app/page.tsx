import DisclaimerBanner from "./components/DisclaimerBanner";
import NavBar from "./components/NavBar";

const domains = [
  { name: "Urinalysis", desc: "pH, specific gravity, protein & glucose flagging from optical strip signals." },
  { name: "HbA1c", desc: "Glycemic-range estimation from electrochemical sensor readings." },
  { name: "Blood Chemistry", desc: "Electrolyte & renal-function panel screening." },
  { name: "Metabolic Panel", desc: "Glucose, calcium, CO2 and albumin pattern detection." },
  { name: "HIV Screening", desc: "Immunoassay OD-ratio triage — always confirmatory-test framed." },
];

const pipeline = [
  { step: "01", title: "Preprocess", copy: "Denoise, normalize, and extract features from raw biosensor waveforms." },
  { step: "02", title: "Train", copy: "Fit domain models on synthetic, procedurally generated datasets." },
  { step: "03", title: "Infer", copy: "Score a new sample and attach a confidence value to every finding." },
  { step: "04", title: "Evaluate", copy: "Continuously benchmark accuracy, F1, and ROC-AUC against held-out sets." },
];

const stack = [
  "Next.js 15 + TypeScript", "FastAPI", "PyTorch / TensorFlow / XGBoost", "PostgreSQL + Redis",
  "S3-compatible storage", "Kubernetes + Terraform", "Prometheus + Grafana", "OpenSearch",
];

export default function MarketingPage() {
  return (
    <main className="min-h-screen bg-trace-grid bg-[length:32px_32px]">
      <DisclaimerBanner />
      <NavBar />

      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 pb-20 pt-16 md:pt-24">
        <div className="grid items-center gap-12 md:grid-cols-2">
          <div>
            <p className="mb-4 font-mono text-xs uppercase tracking-[0.2em] text-signal-500">
              Research prototype · synthetic data only
            </p>
            <h1 className="font-display text-4xl font-semibold leading-[1.1] tracking-tight text-mist-100 md:text-5xl">
              From raw signal
              <br />
              to <span className="text-signal-500">structured insight.</span>
            </h1>
            <p className="mt-6 max-w-md text-mist-300">
              EQUIDX AI demonstrates what a modular, AI-assisted biosensor
              diagnostics platform could look like — architecture, pipelines,
              and interfaces built to production-engineering standards, with
              every model trained on synthetic data for demonstration only.
            </p>
            <div className="mt-8 flex gap-4">
              <a href="/register" className="rounded-full bg-signal-500 px-6 py-3 text-sm font-medium text-ink-950 hover:bg-signal-400">
                Request research access
              </a>
              <a href="#pipeline" className="rounded-full border border-ink-600 px-6 py-3 text-sm text-mist-100 hover:border-signal-500">
                See the pipeline
              </a>
            </div>
          </div>

          {/* Signature: oscilloscope trace */}
          <div className="rounded-2xl border border-ink-600 bg-ink-950/60 p-6">
            <div className="mb-3 flex items-center justify-between font-mono text-xs text-mist-500">
              <span>EQX-Gly2 · live synthetic trace</span>
              <span className="text-signal-500">● streaming</span>
            </div>
            <svg viewBox="0 0 400 140" className="w-full">
              <polyline
                fill="none"
                stroke="#3DDC97"
                strokeWidth="1.5"
                points="0,80 15,78 30,82 45,70 60,90 75,60 90,85 105,75 120,95 135,55 150,88 165,72 180,100 195,65 210,80 225,50 240,92 255,68 270,78 285,60 300,85 315,73 330,95 345,58 360,82 375,70 400,80"
              />
              <line x1="0" y1="70" x2="400" y2="70" stroke="#22332E" strokeWidth="1" strokeDasharray="4 4" />
            </svg>
            <div className="mt-4 grid grid-cols-3 gap-4 font-mono text-xs">
              <div>
                <p className="text-mist-500">HbA1c</p>
                <p className="text-lg text-signal-400">5.7%</p>
              </div>
              <div>
                <p className="text-mist-500">Band</p>
                <p className="text-lg text-amber-400">prediabetic</p>
              </div>
              <div>
                <p className="text-mist-500">Confidence</p>
                <p className="text-lg text-signal-400">0.82</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Domains */}
      <section id="platform" className="border-t border-ink-700 bg-ink-950/40 py-20">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="font-display text-2xl font-semibold text-mist-100">Five diagnostic domains, one framework</h2>
          <p className="mt-2 max-w-xl text-mist-300">
            Every domain implements the same preprocessing → training →
            inference → evaluation contract, so new assays can be added
            without touching the surrounding platform.
          </p>
          <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {domains.map((d) => (
              <div key={d.name} className="rounded-xl border border-ink-600 p-5 hover:border-signal-600">
                <h3 className="font-display text-base font-medium text-signal-400">{d.name}</h3>
                <p className="mt-2 text-sm text-mist-300">{d.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pipeline */}
      <section id="pipeline" className="py-20">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="font-display text-2xl font-semibold text-mist-100">The inference pipeline</h2>
          <div className="mt-10 grid gap-6 md:grid-cols-4">
            {pipeline.map((p) => (
              <div key={p.step} className="border-l border-ink-600 pl-4">
                <p className="font-mono text-xs text-signal-500">{p.step}</p>
                <h3 className="mt-1 font-display text-lg text-mist-100">{p.title}</h3>
                <p className="mt-2 text-sm text-mist-300">{p.copy}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stack */}
      <section className="border-t border-ink-700 py-16">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="font-display text-xl font-semibold text-mist-100">Built on</h2>
          <div className="mt-6 flex flex-wrap gap-3 font-mono text-xs text-mist-300">
            {stack.map((s) => (
              <span key={s} className="rounded-full border border-ink-600 px-3 py-1.5">{s}</span>
            ))}
          </div>
        </div>
      </section>

      <footer className="border-t border-ink-700 py-10 text-center text-xs text-mist-500">
        EQUIDX AI is a research/demo project. Not affiliated with any real
        diagnostics manufacturer. © 2026.
      </footer>
    </main>
  );
}
