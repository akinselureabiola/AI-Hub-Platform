import type { ReactNode } from "react";
import "./globals.css";

const navLinks = [
  { label: "Home", href: "/" },
  { label: "Features", href: "#features" },
  { label: "Docs", href: "#docs" },
];

export const metadata = {
  title: "AI Hub Platform",
  description: "A clean dark-mode ready Supabase-powered app layout.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased">
        <div className="min-h-screen flex flex-col">
          <header className="bg-slate-900/95 border-b border-slate-800 backdrop-blur-sm sticky top-0 z-40">
            <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-4 sm:px-6">
              <a href="/" className="text-lg font-semibold tracking-tight text-slate-50">
                AI Hub
              </a>
              <nav className="hidden items-center gap-6 md:flex">
                {navLinks.map((item) => (
                  <a
                    key={item.href}
                    href={item.href}
                    className="text-sm font-medium text-slate-300 transition hover:text-white"
                  >
                    {item.label}
                  </a>
                ))}
              </nav>
            </div>
          </header>

          <main className="flex-1 mx-auto w-full max-w-7xl px-4 py-10 sm:px-6">
            <section className="rounded-3xl border border-slate-800/70 bg-slate-900/80 p-8 shadow-[0_20px_70px_-30px_rgba(15,23,42,0.7)] backdrop-blur-xl">
              {children}
            </section>
          </main>
        </div>
      </body>
    </html>
  );
}
