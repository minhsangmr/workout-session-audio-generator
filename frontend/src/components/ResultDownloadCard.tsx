"use client";

import { CheckCircle2, Download, RotateCcw, Play } from "lucide-react";
import { getDownloadUrl } from "@/lib/api";
import type { GenerateAudioResponse } from "@/types/api";

interface ResultDownloadCardProps {
  result: GenerateAudioResponse;
  onStartOver: () => void;
}

export default function ResultDownloadCard({
  result,
  onStartOver,
}: ResultDownloadCardProps) {
  const downloadUrl = getDownloadUrl(result.download_url);

  const handleOpenAudio = () => {
    window.open(downloadUrl, "_blank");
  };

  return (
    <div className="glass-card rounded-3xl p-6 md:p-8 border border-green-500/20 bg-gradient-to-br from-green-500/5 to-transparent">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-400 to-emerald-600 p-3">
          <CheckCircle2 className="w-full h-full text-white" />
        </div>
        <div>
          <h2 className="text-xl font-semibold text-green-400">
            Your workout audio is ready
          </h2>
          <p className="text-sm text-white/40">
            Step 4 — Download or play your MP3
          </p>
        </div>
      </div>

      {/* Result info */}
      <div className="glass-card rounded-2xl p-5 mb-6 space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-sm text-white/50">Output file</span>
          <span className="text-sm font-medium text-white/80">
            {result.output_file}
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-sm text-white/50">File ID</span>
          <span className="text-sm font-medium text-white/60 font-mono">
            {result.file_id.slice(0, 12)}...
          </span>
        </div>
      </div>

      {/* Actions */}
      <div className="flex flex-col sm:flex-row gap-3">
        <a
          href={downloadUrl}
          download
          className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-sm transition-all duration-200 bg-gradient-to-r from-green-500 to-emerald-600 text-white shadow-lg shadow-green-500/20 hover:shadow-green-500/40 hover:scale-[1.02] active:scale-[0.98]"
        >
          <Download className="w-4 h-4" />
          Download MP3
        </a>
        <button
          onClick={handleOpenAudio}
          className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-sm transition-all duration-200 glass-card-hover"
        >
          <Play className="w-4 h-4" />
          Open audio
        </button>
      </div>

      {/* Start over */}
      <button
        onClick={onStartOver}
        className="mt-4 w-full inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-medium text-sm transition-all duration-200 text-white/40 hover:text-white/70 hover:bg-white/[0.03]"
      >
        <RotateCcw className="w-4 h-4" />
        Start over
      </button>
    </div>
  );
}