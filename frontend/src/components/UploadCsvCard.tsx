"use client";

import { useState, useRef } from "react";
import { Upload, File, X } from "lucide-react";
import { cn, truncateFileId } from "@/lib/utils";
import { uploadCsv } from "@/lib/api";
import type { UploadResponse } from "@/types/api";
import StatusBadge, { type StatusType } from "./StatusBadge";

interface UploadCsvCardProps {
  onUploadSuccess: (fileId: string) => void;
}

export default function UploadCsvCard({ onUploadSuccess }: UploadCsvCardProps) {
  const [file, setFile] = useState<File | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [status, setStatus] = useState<StatusType>("idle");
  const [message, setMessage] = useState("");
  const [uploadResult, setUploadResult] = useState<UploadResponse | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const isValidFile = (f: File) => f.name.endsWith(".csv");

  const handleFileSelect = (f: File) => {
    if (!isValidFile(f)) {
      setStatus("error");
      setMessage("Please select a CSV file");
      return;
    }
    setFile(f);
    setStatus("idle");
    setMessage("");
    setUploadResult(null);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFileSelect(f);
  };

  const handleUpload = async () => {
    if (!file) return;
    setStatus("loading");
    setMessage("Uploading...");
    try {
      const result = await uploadCsv(file);
      setUploadResult(result);
      setStatus("success");
      setMessage(`Uploaded: ${result.filename}`);
      onUploadSuccess(result.file_id);
    } catch (err: unknown) {
      setStatus("error");
      if (err instanceof Error) {
        setMessage(err.message);
      } else {
        setMessage("Upload failed. Is the backend running?");
      }
    }
  };

  const handleReset = () => {
    setFile(null);
    setUploadResult(null);
    setStatus("idle");
    setMessage("");
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div className="glass-card rounded-3xl p-6 md:p-8">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-cyan-600 p-2.5">
          <Upload className="w-full h-full text-white" />
        </div>
        <div>
          <h2 className="text-xl font-semibold">Upload CSV</h2>
          <p className="text-sm text-white/40">
            Step 1 — Upload your workout plan
          </p>
        </div>
      </div>

      {/* Drop zone */}
      {!uploadResult && (
        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          className={cn(
            "border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200",
            dragOver
              ? "border-cyan-400 bg-cyan-500/5"
              : "border-white/10 hover:border-white/20 hover:bg-white/[0.02]"
          )}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".csv"
            className="hidden"
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (f) handleFileSelect(f);
            }}
          />
          <Upload className="w-10 h-10 mx-auto mb-3 text-white/30" />
          <p className="font-medium mb-1">Drop CSV file here or click to browse</p>
          <p className="text-sm text-white/30">Only .csv files accepted</p>
        </div>
      )}

      {/* Selected file */}
      {file && !uploadResult && (
        <div className="mt-4 flex items-center justify-between glass-card rounded-xl p-3">
          <div className="flex items-center gap-3">
            <File className="w-5 h-5 text-cyan-400" />
            <div>
              <p className="text-sm font-medium">{file.name}</p>
              <p className="text-xs text-white/40">
                {(file.size / 1024).toFixed(1)} KB
              </p>
            </div>
          </div>
          <button
            onClick={handleReset}
            className="p-1.5 rounded-lg hover:bg-white/5 transition-colors"
          >
            <X className="w-4 h-4 text-white/40" />
          </button>
        </div>
      )}

      {/* Upload success info */}
      {uploadResult && (
        <div className="mt-4 glass-card rounded-xl p-4 border border-green-500/20 bg-green-500/5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <File className="w-5 h-5 text-green-400" />
              <div>
                <p className="text-sm font-medium">{uploadResult.filename}</p>
                <p className="text-xs text-white/40">
                  ID: {truncateFileId(uploadResult.file_id)}
                </p>
              </div>
            </div>
            <button
              onClick={handleReset}
              className="p-1.5 rounded-lg hover:bg-white/5 transition-colors"
            >
              <X className="w-4 h-4 text-white/40" />
            </button>
          </div>
        </div>
      )}

      {/* Status */}
      <StatusBadge status={status} message={message} />

      {/* Upload button */}
      {file && !uploadResult && (
        <div className="mt-4">
          <button
            onClick={handleUpload}
            disabled={status === "loading"}
            className="w-full inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl font-semibold text-sm transition-all duration-200 bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/40 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            {status === "loading" && (
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            )}
            {status === "loading" ? "Uploading..." : "Upload CSV"}
          </button>
        </div>
      )}
    </div>
  );
}