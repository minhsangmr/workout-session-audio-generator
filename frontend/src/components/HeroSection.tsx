"use client";

import { ArrowRight, PlayCircle } from "lucide-react";
import Link from "next/link";

export default function HeroSection() {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden px-4">
      {/* Background gradient orbs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -left-40 w-[80vh] h-[80vh] rounded-full bg-cyan-500/10 blur-[120px]" />
        <div className="absolute -bottom-40 -right-40 w-[80vh] h-[80vh] rounded-full bg-violet-500/10 blur-[120px]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60vh] h-[60vh] rounded-full bg-blue-500/5 blur-[100px]" />
      </div>

      {/* Grid pattern overlay */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
        }}
      />

      <div className="relative z-10 max-w-4xl mx-auto text-center">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass-card text-sm text-white/60 mb-8">
          <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          AI-Powered Workout Audio Generator
        </div>

        <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold tracking-tight leading-tight mb-6">
          Turn your workout plan
          <br />
          <span className="gradient-text">into guided audio</span>
        </h1>

        <p className="text-lg md:text-xl text-white/50 max-w-2xl mx-auto mb-10 leading-relaxed">
          Upload a CSV workout plan, generate Vietnamese voice coaching,
          add beeps and background music, then download a ready-to-play MP3
          session.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="/generator"
            className="group inline-flex items-center gap-2 px-8 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold text-lg shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 hover:scale-105 transition-all duration-300"
          >
            Create workout audio
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>

          <Link
            href="#workflow"
            className="group inline-flex items-center gap-2 px-8 py-4 rounded-2xl glass-card-hover text-white/80 font-medium text-lg"
          >
            <PlayCircle className="w-5 h-5" />
            View sample flow
          </Link>
        </div>
      </div>
    </section>
  );
}