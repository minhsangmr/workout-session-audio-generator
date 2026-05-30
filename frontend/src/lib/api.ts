import type {
  UploadResponse,
  PreviewResponse,
  GenerateAudioRequest,
  GenerateAudioResponse,
} from "@/types/api";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

class ApiError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      if (body.detail) {
        detail = body.detail;
      }
    } catch {
      // ignore JSON parse errors
    }
    throw new ApiError(response.status, detail);
  }
  return response.json();
}

export async function healthCheck(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/health`, {
    method: "GET",
  });
  return handleResponse(response);
}

export async function uploadCsv(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload-csv`, {
    method: "POST",
    body: formData,
  });
  return handleResponse<UploadResponse>(response);
}

export async function previewWorkout(
  fileId: string
): Promise<PreviewResponse> {
  const response = await fetch(`${API_BASE_URL}/preview`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ file_id: fileId }),
  });
  return handleResponse<PreviewResponse>(response);
}

export async function generateAudio(
  payload: GenerateAudioRequest
): Promise<GenerateAudioResponse> {
  const response = await fetch(`${API_BASE_URL}/generate-audio`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<GenerateAudioResponse>(response);
}

export function getDownloadUrl(downloadUrl: string): string {
  if (downloadUrl.startsWith("http")) {
    return downloadUrl;
  }
  return `${API_BASE_URL}${downloadUrl}`;
}

export { ApiError };