import Link from "next/link";
import NavBar from "../../components/NavBar";
import DisclaimerBanner from "../../components/DisclaimerBanner";

const architecture = [
  ["01", "Experience", "Next.js app router, typed API client, role-aware dashboard, and a deliberately explicit research-use boundary."],
  ["02", "Application", "FastAPI services own authentication, sample lifecycle, report orchestration, health checks, and audit-oriented seams."],
  ["03", "Inference", "The AI engine is isolated behind a service boundary so model code can evolve without coupling the clinical workflow to one implementation."],
  ["04", "Evidence", "Analytics, simulator, and integration tests make the system observable before any claim is made about clinical performance."],
];

const principles = [
  { title: "Provenance is a feature", body: "A result is only as useful as the chain behind it. EquiDx keeps sample identity, status, model version, and report context close to the workflow instead of treating them as metadata to add later." },
  { title: "Boundaries beat cleverness", body: "Inference, persistence, transport, and presentation are separate concerns. That gives the team smaller surfaces to test and clearer failure behavior when a dependency is unavailable." },
  { title: "Interpretability is operational", body: "Confidence, limitations, review states, and research disclaimers are part of the product surface. They are not a post-processing paragraph added after the model is trained." },
];

const delivery = [
  "Define intended use and data contracts before expanding model scope.",
  "Validate against representative clinical data with independent, leakage-safe splits.",
  "Add reproducible model artifacts, SBOMs, signed releases, and rollback paths.",
  "Run full-stack integration and browser workflows, not only unit tests.",
  "Move from research prototype to regulated product only through a controlled QMS and evidence plan.",
];

export default function EquiDxEngineeringPage() {
  return (
    <main className="min-h-screen bg-ink-900">
      <DisclaimerBanner />
      <NavBar />
      <article>
        <header className="border-b border-ink-700 bg-trace-grid">
          <div className="mx-auto max-w-5xl px-6 pb-20 pt-14 lg:pb-28 lg:pt-20">
            <Link href="/" className="font-mono text-xs uppercase tracking-[0.28em] text-signal-400">← Back to EquiDx AI</Link>
            <div className="mt-12 max-w-4xl">
              <p className="font-mono text-xs uppercase tracking-[0.28em] text-mist-500">Technical note / systems engineering</p>
              <h1 className="mt-5 font-display text-5xl font-semibold tracking-tight text-mist-100 sm:text-7xl">Building EquiDx AI as an auditable biosensor research platform.</h1>
              <p className="mt-7 max-w-3xl text-xl leading-9 text-mist-300">The engineering challenge is not to wrap a model in a dashboard. It is to connect signal provenance, workflow state, inference, review, and operational evidence without pretending that a prototype is a clinical device.</p>
            </div>
            <div className="mt-12 flex flex-wrap gap-x-10 gap-y-4 border-t border-ink-700 pt-5 font-mono text-xs uppercase tracking-widest text-mist-500">
              <span>Systems design</span><span>AI boundaries</span><span>Clinical safety posture</span><span>Research use only</span>
            </div>
          </div>
        </header>

        <div className="mx-auto grid max-w-5xl gap-16 px-6 py-16 lg:grid-cols-[1fr_0.34fr] lg:py-24">
          <div className="space-y-14 text-mist-300">
            <section>
              <p className="font-mono text-xs uppercase tracking-[0.28em] text-signal-400">01 / The problem</p>
              <h2 className="mt-4 font-display text-3xl text-mist-100">Clinical-looking interfaces can hide engineering gaps.</h2>
              <p className="mt-6 leading-8">A biosensor pipeline has to do more than produce a score. It has to associate the right signal with the right sample, preserve state as that sample moves through a workflow, make the inference step inspectable, and tell a reviewer what the output does—and does not—mean.</p>
              <p className="mt-5 leading-8">That is the design problem behind EquiDx AI. The repository is intentionally structured as a small platform: a web experience, a FastAPI application layer, an isolated AI engine, a biosensor simulator, analytics, and a mobile-facing service. The seams matter because they make assumptions visible.</p>
            </section>

            <section>
              <p className="font-mono text-xs uppercase tracking-[0.28em] text-signal-400">02 / Architecture</p>
              <h2 className="mt-4 font-display text-3xl text-mist-100">Keep the path modular, keep the evidence close.</h2>
              <div className="mt-8 grid gap-3 sm:grid-cols-2">
                {architecture.map(([number, title, body]) => (
                  <div key={number} className="rounded-2xl border border-ink-700 bg-ink-800/50 p-5">
                    <span className="font-mono text-xs text-signal-400">{number}</span>
                    <h3 className="mt-7 font-display text-xl text-mist-100">{title}</h3>
                    <p className="mt-3 text-sm leading-6 text-mist-500">{body}</p>
                  </div>
                ))}
              </div>
              <div className="mt-8 rounded-2xl border border-signal-500/30 bg-ink-950 p-5 font-mono text-xs leading-7 text-mist-300">
                <p><span className="text-signal-400">input</span> → sample identity → lifecycle state</p>
                <p>          ↓</p>
                <p><span className="text-signal-400">features</span> → model boundary → confidence + limitations</p>
                <p>          ↓</p>
                <p><span className="text-signal-400">report</span> → human review → audit / analytics</p>
              </div>
            </section>

            <section>
              <p className="font-mono text-xs uppercase tracking-[0.28em] text-signal-400">03 / Design principles</p>
              <div className="mt-6 space-y-7">
                {principles.map((principle, index) => (
                  <div key={principle.title} className="grid gap-4 border-t border-ink-700 pt-6 sm:grid-cols-[3rem_1fr]">
                    <span className="font-mono text-xs text-mist-500">0{index + 1}</span>
                    <div><h3 className="font-display text-xl text-mist-100">{principle.title}</h3><p className="mt-3 leading-7">{principle.body}</p></div>
                  </div>
                ))}
              </div>
            </section>

            <section>
              <p className="font-mono text-xs uppercase tracking-[0.28em] text-signal-400">04 / What is verified</p>
              <h2 className="mt-4 font-display text-3xl text-mist-100">A tested foundation, not a clinical claim.</h2>
              <p className="mt-6 leading-8">The repository exercises backend authentication and sample behavior, AI-engine inference paths, biosensor signal generation, analytics aggregation, mobile API behavior, cross-service flags, and the frontend production build. Security hardening includes fail-closed production configuration and protection against privileged self-registration.</p>
              <p className="mt-5 leading-8">Those checks establish engineering behavior. They do not establish sensitivity, specificity, clinical utility, regulatory clearance, or fitness for patient care. The distinction is deliberate: a reliable software foundation is necessary for clinical validation, but it is not clinical validation.</p>
            </section>

            <section>
              <p className="font-mono text-xs uppercase tracking-[0.28em] text-signal-400">05 / The path forward</p>
              <h2 className="mt-4 font-display text-3xl text-mist-100">Move from prototype to evidence in the right order.</h2>
              <ol className="mt-7 space-y-4">
                {delivery.map((item, index) => <li key={item} className="flex gap-4 rounded-xl border border-ink-700 px-5 py-4 text-sm leading-6"><span className="font-mono text-signal-400">0{index + 1}</span><span>{item}</span></li>)}
              </ol>
            </section>
          </div>

          <aside className="lg:sticky lg:top-8 lg:self-start">
            <div className="rounded-2xl border border-amber-500/30 bg-amber-500/5 p-6">
              <p className="font-mono text-xs uppercase tracking-[0.2em] text-amber-400">Boundary condition</p>
              <p className="mt-5 text-sm leading-7 text-mist-300">EquiDx AI is an early-stage research and demonstration platform. It uses synthetic data and placeholder models, has not been clinically validated, and is not a medical device.</p>
              <Link href="/disclaimer" className="mt-5 inline-block text-sm text-amber-400 trace-underline">Read the full disclaimer ↗</Link>
            </div>
            <div className="mt-5 rounded-2xl border border-ink-700 p-6">
              <p className="font-mono text-xs uppercase tracking-[0.2em] text-mist-500">Repository map</p>
              <ul className="mt-5 space-y-3 font-mono text-xs text-mist-300">
                <li><span className="text-signal-400">/backend</span> application + auth</li>
                <li><span className="text-signal-400">/ai-engine</span> inference boundary</li>
                <li><span className="text-signal-400">/biosensor-simulator</span> signal generation</li>
                <li><span className="text-signal-400">/analytics</span> operational rollups</li>
                <li><span className="text-signal-400">/web</span> research dashboard</li>
              </ul>
            </div>
          </aside>
        </div>
      </article>
      <footer className="border-t border-ink-700 px-6 py-10 text-center font-mono text-xs uppercase tracking-widest text-mist-500">EquiDx AI / engineering note / synthetic data only</footer>
    </main>
  );
}
