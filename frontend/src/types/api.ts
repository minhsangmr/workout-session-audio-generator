export interface UploadResponse {
  file_id: string;
  filename: string;
  stored_path: string;
}

export interface PreviewResponse {
  file_id: string;
  script: string;
  total_exercises: number;
}

export interface GenerateAudioRequest {
  file_id: string;
  tts_engine: string;
  timeline_mode: boolean;
  beep: boolean;
  work_beep_offsets: number[];
  rest_beep_offsets: number[];
  background_music: string | null;
  voice_music_volume_db: number;
  active_music_volume_db: number;
  fade_in_ms: number;
  fade_out_ms: number;
}

export interface GenerateAudioResponse {
  file_id: string;
  output_file: string;
  download_url: string;
}
