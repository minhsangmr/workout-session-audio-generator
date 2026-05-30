"use client";

import { useState, useCallback } from "react";
import UploadCsvCard from "@/components/UploadCsvCard";
import PreviewScriptCard from "@/components/PreviewScriptCard";
import GenerateSettingsCard from "@/components/GenerateSettingsCard";
import ResultDownloadCard from "@/components/ResultDownloadCard";
import type { GenerateAudioResponse } from "@/types/api";

type Step = "upload" | "preview" | "generate" | "result";

const STEP_LABELS = ["Upload", "Preview", "Configure", "Download"];

export default function GeneratorPage() {
  const [fileId, setFileId] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState<Step>("upload");
  const [generateResult, setGenerateResult] =
    useState<GenerateAudioResponse | null>(null);

  const handleUploadSuccess = useCallback((id: string) => {
    setFileId(id);
    setCurrentStep("preview");
  }, []);

  const handlePreviewComplete = useCallback(() => {
    setCurrentStep("generate");
  }, []);

  const handleGenerateSuccess = useCallback(
    (result: GenerateAudioResponse) => {
      setGenerateResult(result);
      setCurrentStep("result");
    },
    []
  );

  const handleStartOver = useCallback(() => {
    setFileId(null);
    setGenerateResult(null);
    setCurrentStep("upload");
  }, []);

  const stepIndex = ["upload", "preview", "generate", "result"].indexOf(currentStep);

  return (
    <div className="relative min-h-screen py-12 px-4">
      {/* Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-[60vh] h-[60vh] rounded-full bg-violet-500/10 blur-[120px]" />
        <div className="absolute -bottom-40 -left-40 w-[60vh] h-[60vh] rounded-full bg-cyan-500/10 blur-[120px]" />
      </div>

      <div className="relative z-10 max-w-3xl mx-auto">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-3xl md:text-5xl font-bold mb-3">
            Audio Generator
          </h1>
          <p className="text-white/50 text-lg">
            Upload, preview, configure, and download your workout audio.
          </p>
        </div>

        {/* Step indicators */}
        <div className="flex items-center justify-center gap-2 mb-10">
          {(["upload", "preview", "generate", "result"] as const).map(
            (step, index) => {
              const isActive = index === stepIndex;
              const isCompleted = index < stepIndex;

              return (
                <div key={step} className="flex items-center gap-2">
                  <div className="flex items-center gap-2">
                    <div
                      className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                        isCompleted
                          ? "bg-gradient-to-r from-cyan-500 to-blue-600 text-white"
                          : isActive
                          ? "bg-white/10 text-white border border-white/20"
                          : "bg-white/[0.03] text-white/30 border border-white/5"
                      }`}
                    >
                      {isCompleted ? (
                        <svg
                          className="w-4 h-4"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2.5}
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                      ) : (
                        index + 1
                      )}
                    </div>
                    <span
                      className={`text-xs font-medium hidden sm:block ${
                        isActive || isCompleted
                          ? "text-white/70"
                          : "text-white/30"
                      }`}
                    >
                      {STEP_LABELS[index]}
                    </span>
                  </div>
                  {index < 3 && (
                    <div
                      className={`w-8 h-px ${
                        isCompleted ? "bg-cyan-500/50" : "bg-white/5"
                      }`}
                    />
                  )}
                </div>
              );
            }
          )}
        </div>

        {/* Card stack */}
        <div className="space-y-6">
          {/* Step 1: Upload — always visible */}
          <UploadCsvCard onUploadSuccess={handleUploadSuccess} />

          {/* Step 2: Preview — visible when file is uploaded */}
          {fileId && (
            <PreviewScriptCard
              fileId={fileId}
              onPreviewComplete={handlePreviewComplete}
            />
          )}

          {/* Step 3: Generate — visible after preview is done */}
          {(currentStep === "generate" || currentStep === "result") && fileId && (
            <GenerateSettingsCard
              fileId={fileId}
              onGenerateSuccess={handleGenerateSuccess}
            />
          )}

          {/* Step 4: Result */}
          {currentStep === "result" && generateResult && (
            <ResultDownloadCard
              result={generateResult}
              onStartOver={handleStartOver}
            />
          )}
        </div>
      </div>
    </div>
  );
}