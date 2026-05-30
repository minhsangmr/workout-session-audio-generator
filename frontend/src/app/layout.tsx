import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { Dumbbell } from "lucide-react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Workout Session Audio Generator",
  description:
    "Turn your workout plan into guided audio. Upload a CSV, generate Vietnamese voice coaching, add beeps and background music, then download a ready-to-play MP3 session.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={inter.className}>
        {/* Navbar */}
        <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0a1a]/80 backdrop-blur-xl border-b border-white/[0.04]">
          <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
            <Link
              href="/"
              className="flex items-center gap-2.5 group"
            >
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-400 to-blue-600 p-1.5 shadow-lg shadow-cyan-500/20 group-hover:scale-105 transition-transform">
                <Dumbbell className="w-full h-full text-white" />
              </div>
              <span className="font-semibold text-sm hidden sm:block">
                Workout Audio
              </span>
            </Link>
            <div className="flex items-center gap-4">
              <Link
                href="/"
                className="text-sm text-white/50 hover:text-white/80 transition-colors"
              >
                Home
              </Link>
              <Link
                href="/generator"
                className="text-sm px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-medium shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/40 transition-all duration-200"
              >
                Generator
              </Link>
            </div>
          </div>
        </nav>

        {/* Main content */}
        <main className="min-h-screen pt-16">{children}</main>

        {/* Footer */}
        <footer className="border-t border-white/[0.04] py-8 px-4">
          <div className="max-w-6xl mx-auto text-center">
            <p className="text-sm text-white/30">
              Workout Session Audio Generator &mdash; Built with Next.js & FastAPI
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}