"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, Users, TestTube2, FileText, BarChart3, ShieldCheck } from "lucide-react";

const nav = [
  { href: "/dashboard", label: "Overview", icon: LayoutDashboard },
  { href: "/dashboard/patients", label: "Patients", icon: Users },
  { href: "/dashboard/samples", label: "Samples", icon: TestTube2 },
  { href: "/dashboard/reports", label: "Reports", icon: FileText },
  { href: "/dashboard/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/admin", label: "Admin", icon: ShieldCheck },
];

export default function DashboardShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  return (
    <div className="flex min-h-screen bg-ink-900">
      <aside className="w-60 shrink-0 border-r border-ink-700 p-6">
        <Link href="/" className="font-display text-lg font-semibold text-mist-100">
          EQUIDX <span className="text-signal-500">AI</span>
        </Link>
        <nav className="mt-8 space-y-1">
          {nav.map(({ href, label, icon: Icon }) => {
            const active = pathname === href;
            return (
              <Link
                key={href} href={href}
                className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm ${
                  active ? "bg-ink-700 text-signal-400" : "text-mist-300 hover:bg-ink-800 hover:text-mist-100"
                }`}
              >
                <Icon size={16} />
                {label}
              </Link>
            );
          })}
        </nav>
        <div className="mt-10 rounded-lg border border-amber-500/30 bg-amber-500/5 p-3 text-xs text-amber-400">
          Research Prototype — synthetic data, placeholder AI models. Not for
          clinical use.
        </div>
      </aside>
      <div className="flex-1">
        <header className="flex items-center justify-between border-b border-ink-700 px-8 py-4">
          <p className="font-mono text-xs uppercase tracking-widest text-mist-500">
            Research Dashboard
          </p>
          <div className="flex items-center gap-3 text-sm text-mist-300">
            <span className="h-2 w-2 rounded-full bg-signal-500" /> Synthetic environment
          </div>
        </header>
        <main className="p-8">{children}</main>
      </div>
    </div>
  );
}
