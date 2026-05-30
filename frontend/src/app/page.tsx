import HeroSection from "@/components/HeroSection";
import FeatureGrid from "@/components/FeatureGrid";
import WorkflowSteps from "@/components/WorkflowSteps";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

export default function HomePage() {
  return (
    <>
      <HeroSection />
      <FeatureGrid />
      <WorkflowSteps />

      {/* Final CTA section */}
      <section className="relative py-24 px-4">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60vh] h-[60vh] rounded-full bg-cyan-500/10 blur-[120px]" />
        </div>
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-bold mb-4">
            Ready to create your workout audio?
          </h2>
          <p className="text-white/50 text-lg mb-8 max-w-xl mx-auto">
            Upload your CSV plan and get a professional guided audio session in minutes.
          </p>
          <Link
            href="/generator"
            className="inline-flex items-center gap-2 px-8 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold text-lg shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 hover:scale-105 transition-all duration-300"
          >
            Get started
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>
    </>
  );
}