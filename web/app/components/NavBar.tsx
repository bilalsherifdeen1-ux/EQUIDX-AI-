import Link from "next/link";

const links = [
  { href: "/#platform", label: "Platform" },
  { href: "/#pipeline", label: "AI Pipeline" },
  { href: "/dashboard", label: "Dashboard" },
];

export default function NavBar() {
  return (
    <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
      <Link href="/" className="font-display text-lg font-semibold tracking-tight text-mist-100">
        EQUIDX <span className="text-signal-500">AI</span>
      </Link>
      <div className="hidden gap-8 font-body text-sm text-mist-300 md:flex">
        {links.map((l) => (
          <Link key={l.href} href={l.href} className="trace-underline hover:text-signal-400">
            {l.label}
          </Link>
        ))}
      </div>
      <div className="flex gap-3">
        <Link
          href="/login"
          className="rounded-full border border-ink-600 px-4 py-2 text-sm text-mist-100 hover:border-signal-500 hover:text-signal-400"
        >
          Sign in
        </Link>
        <Link
          href="/register"
          className="rounded-full bg-signal-500 px-4 py-2 text-sm font-medium text-ink-950 hover:bg-signal-400"
        >
          Request access
        </Link>
      </div>
    </nav>
  );
}
