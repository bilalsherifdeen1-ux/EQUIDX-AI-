export default function DisclaimerBanner() {
  return (
    <div className="w-full border-b border-ink-600 bg-ink-950/80 px-4 py-2 text-center text-xs text-mist-500">
      Research prototype — synthetic data only. Not a medical device. Not for
      clinical diagnosis.{" "}
      <a href="/disclaimer" className="trace-underline text-signal-500">
        Learn more
      </a>
    </div>
  );
}
