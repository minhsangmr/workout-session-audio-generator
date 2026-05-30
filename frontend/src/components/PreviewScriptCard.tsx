"use client";

import { useState } from "react";
import { FileText, Eye } from "lucide-react";
import { previewWorkout } from "@/lib/api";
import type { PreviewResponse } from "@/types/api";
import StatusBadge, { type StatusType } from "./StatusBadge";

interface PreviewScriptCardProps {
  fileId: string;
  onPreviewComplete?: () => void;
}

export default function PreviewScriptCard({ fileId, onPreviewComplete }: PreviewScriptCardProps) {
  const [preview, setPreview] = useState<PreviewResponse | null>(null);
  const [status, setStatus] = useState<StatusType>("idle");
  const [message, setMessage] = useState("");

  const handlePreview = async () => {
    setStatus("loading");
    setMessage("Loading script...");
    try {
      const result = await previewWorkout(fileId);
      setPreview(result);
      setStatus("success");
      setMessage(`${result.total_exercises} exercise(s) found`);
      onPreviewComplete?.();
    } catch (err: unknown) {
      setStatus("error");
      if (err instanceof Error) {
        setMessage(err.message);
      } else {
        setMessage("Failed to preview script");
      }
    }
  };

  return (
    <div className="glass-card rounded-3xl p-6 md:p-8">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-400 to-blue-600 p-2.5">
          <FileText className="w-full h-full text-white" />
        </div>
        <div>
          <h2 className="text-xl font-semibold">Preview Script</h2>
          <p className="text-sm text-white/40">Step 2 — Review workout script</p>
        </div>
      </div>

      {/* Preview button */}
      {!preview && (
        <button
          onClick={handlePreview}
          disabled={status === "loading"}
          className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-semibold text-sm transition-all duration-200 glass-card-hover disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {status === "loading" ? (
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <Eye className="w-4 h-4" />
          )}
          {status === "loading" ? "Loading..." : "Preview workout"}
        </button>
      )}

      {/* Script content */}
      {preview && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <StatusBadge status={status} message={message} />
          </div>
          <div className="glass-card rounded-2xl p-4 max-h-[400px] overflow-y-auto custom-scrollbar">
            <pre className="text-sm text-white/70 font-mono whitespace-pre-wrap leading-relaxed">
              {preview.script}
            </pre>
          </div>
        </div>
      )}

      {/* Error state */}
      {status === "error" && !preview && (
        <div className="mt-4">
          <StatusBadge status={status} message={message} />
          <button
            onClick={handlePreview}
            className="mt-2 text-sm text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            Try again
          </button>
        </div>
      )}
    </div>
  );
}