import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "EQUIDX AI — Research Prototype Biosensor Diagnostics Platform",
  description:
    "A modular, AI-assisted biosensor diagnostics platform — early-stage research and demonstration only.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
