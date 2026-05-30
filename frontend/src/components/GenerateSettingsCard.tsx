"use client";

import { useState } from "react";
import { Settings, Music, Bell, Waves } from "lucide-react";
import { generateAudio } from "@/lib/api";
import type { GenerateAudioResponse } from "@/types/api";
import StatusBadge, { type StatusType } from "./StatusBadge";

interface GenerateSettingsCardProps {
  fileId: string;
  onGenerateSuccess: (result: GenerateAudioResponse) => void;
}

export default function GenerateSettingsCard({
  fileId,
  onGenerateSuccess,
}: GenerateSettingsCardProps) {
  const [timelineMode, setTimelineMode] = useState(true);
  const [beep, setBeep] = useState(true);
  const [workBeepOffsets, setWorkBeepOffsets] = useState("5,2");
  const [restBeepOffsets, setRestBeepOffsets] = useState("5,2");
  const [backgroundMusic, setBackgroundMusic] = useState("");
  const [voiceMusicVolumeDb, setVoiceMusicVolumeDb] = useState(-24);
  const [activeMusicVolumeDb, setActiveMusicVolumeDb] = useState(-12);
  const [fadeInMs, setFadeInMs] = useState(1000);
  const [fadeOutMs, setFadeOutMs] = useState(1500);
  const [status, setStatus] = useState<StatusType>("idle");
  const [message, setMessage] = useState("");

  const parseOffsets = (input: string): number[] => {
    return input
      .split(",")
      .map((s) => parseInt(s.trim(), 10))
      .filter((n) => !isNaN(n));
  };

  const handleGenerate = async () => {
    setStatus("loading");
    setMessage("Generating audio...");
    try {
      const result = await generateAudio({
        file_id: fileId,
        tts_engine: "gtts",
        timeline_mode: timelineMode,
        beep,
        work_beep_offsets: parseOffsets(workBeepOffsets),
        rest_beep_offsets: parseOffsets(restBeepOffsets),
        background_music: backgroundMusic || null,
        voice_music_volume_db: voiceMusicVolumeDb,
        active_music_volume_db: activeMusicVolumeDb,
        fade_in_ms: fadeInMs,
        fade_out_ms: fadeOutMs,
      });
      setStatus("success");
      setMessage("Audio generated successfully!");
      onGenerateSuccess(result);
    } catch (err: unknown) {
      setStatus("error");
      if (err instanceof Error) {
        setMessage(err.message);
      } else {
        setMessage("Failed to generate audio");
      }
    }
  };

  const ToggleField = ({
    label,
    description,
    checked,
    onChange,
    icon: Icon,
  }: {
    label: string;
    description: string;
    checked: boolean;
    onChange: (v: boolean) => void;
    icon: React.ElementType;
  }) => (
    <label className="flex items-start gap-3 cursor-pointer group">
      <div className="w-8 h-8 rounded-lg bg-white/[0.04] flex items-center justify-center shrink-0 mt-0.5">
        <Icon className="w-4 h-4 text-white/50" />
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium group-hover:text-white transition-colors">
          {label}
        </p>
        <p className="text-xs text-white/30">{description}</p>
      </div>
      <div
        className={`relative w-11 h-6 rounded-full transition-colors ${
          checked ? "bg-cyan-500" : "bg-white/10"
        }`}
      >
        <div
          className={`absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow-md transition-transform ${
            checked ? "translate-x-5" : ""
          }`}
        />
        <input
          type="checkbox"
          className="sr-only"
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
        />
      </div>
    </label>
  );

  const InputField = ({
    label,
    value,
    onChange,
    placeholder,
    type = "text",
    disabled,
  }: {
    label: string;
    value: string | number;
    onChange: (v: string) => void;
    placeholder?: string;
    type?: string;
    disabled?: boolean;
  }) => (
    <div>
      <label className="block text-xs font-medium text-white/40 mb-1.5">
        {label}
      </label>
      <input
        type={type}
        value={value}
        onChange={(e) => {
          const raw = e.target.value;
          if (type === "number") {
            onChange(raw === "" ? "0" : raw);
          } else {
            onChange(raw);
          }
        }}
        placeholder={placeholder}
        disabled={disabled}
        className="w-full bg-white/[0.04] border border-white/10 rounded-xl px-3 py-2.5 text-sm text-white placeholder-white/20 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
      />
    </div>
  );

  return (
    <div className="glass-card rounded-3xl p-6 md:p-8">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-400 to-violet-600 p-2.5">
          <Settings className="w-full h-full text-white" />
        </div>
        <div>
          <h2 className="text-xl font-semibold">Generate Settings</h2>
          <p className="text-sm text-white/40">
            Step 3 — Configure audio options
          </p>
        </div>
      </div>

      <div className="space-y-6">
        {/* Toggles */}
        <div className="space-y-4">
          <ToggleField
            label="Timeline mode"
            description="Generate structured work/rest timeline"
            checked={timelineMode}
            onChange={setTimelineMode}
            icon={Waves}
          />
          <ToggleField
            label="Beep cues"
            description="Play beep sounds before transitions"
            checked={beep}
            onChange={setBeep}
            icon={Bell}
          />
        </div>

        {/* Divider */}
        <div className="h-px bg-white/5" />

        {/* Input fields */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <InputField
            label="TTS Engine"
            value="gtts"
            onChange={() => {}}
            disabled
          />
          <InputField
            label="Work beep offsets (seconds)"
            value={workBeepOffsets}
            onChange={setWorkBeepOffsets}
            placeholder="5,2"
          />
          <InputField
            label="Rest beep offsets (seconds)"
            value={restBeepOffsets}
            onChange={setRestBeepOffsets}
            placeholder="5,2"
          />
          <InputField
            label="Background music path"
            value={backgroundMusic}
            onChange={setBackgroundMusic}
            placeholder="data/music/background.mp3"
          />
          <InputField
            label="Voice music volume (dB)"
            value={voiceMusicVolumeDb}
            onChange={(v) => setVoiceMusicVolumeDb(Number(v))}
            type="number"
          />
          <InputField
            label="Active music volume (dB)"
            value={activeMusicVolumeDb}
            onChange={(v) => setActiveMusicVolumeDb(Number(v))}
            type="number"
          />
          <InputField
            label="Fade in (ms)"
            value={fadeInMs}
            onChange={(v) => setFadeInMs(Number(v))}
            type="number"
          />
          <InputField
            label="Fade out (ms)"
            value={fadeOutMs}
            onChange={(v) => setFadeOutMs(Number(v))}
            type="number"
          />
        </div>

        {/* Status */}
        <StatusBadge status={status} message={message} />

        {/* Generate button */}
        <button
          onClick={handleGenerate}
          disabled={status === "loading"}
          className="w-full inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-sm transition-all duration-200 bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/40 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
        >
          {status === "loading" && (
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          )}
          <Music className="w-4 h-4" />
          {status === "loading" ? "Generating audio..." : "Generate MP3"}
        </button>

        {/* Retry on error */}
        {status === "error" && (
          <button
            onClick={handleGenerate}
            className="w-full text-sm text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            Try again
          </button>
        )}
      </div>
    </div>
  );
}