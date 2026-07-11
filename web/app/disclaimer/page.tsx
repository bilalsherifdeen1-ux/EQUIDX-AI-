import NavBar from "../components/NavBar";

export default function DisclaimerPage() {
  return (
    <main className="min-h-screen bg-ink-900">
      <NavBar />
      <div className="mx-auto max-w-2xl px-6 py-16">
        <h1 className="font-display text-3xl text-mist-100">Research &amp; Prototype Disclaimer</h1>
        <div className="mt-6 space-y-4 text-sm leading-relaxed text-mist-300">
          <p>
            EQUIDX AI is an early-stage research and demonstration platform.
            It is <strong className="text-amber-400">not a medical device</strong> and
            has not been reviewed, cleared, or approved by the FDA, a
            notified body under the EU IVDR, or any other regulatory
            authority.
          </p>
          <p>
            All patient records, biosensor signals, and diagnostic outputs
            produced by this platform are <strong className="text-signal-400">synthetic</strong>,
            generated for demonstration purposes. No component of this
            system has been clinically validated.
          </p>
          <p>
            Nothing produced by EQUIDX AI — including any &ldquo;diagnostic
            report,&rdquo; risk band, or confidence score — may be used to
            diagnose, treat, or make real clinical decisions about a real
            person. Any resemblance between synthetic outputs and real
            clinical findings is coincidental.
          </p>
          <p>
            If you are experiencing a medical concern, please consult a
            licensed healthcare professional.
          </p>
        </div>
      </div>
    </main>
  );
}
