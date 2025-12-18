import { Preferences, TranslateResponse } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

function getClientId(): string {
  if (typeof window === "undefined") return "";
  let id = localStorage.getItem("client_id");
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem("client_id", id);
  }
  return id;
}

export function getSavedPreferences(): Preferences | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("prefs");
  if (!raw) return null;
  try { return JSON.parse(raw) as Preferences; } catch { return null; }
}

export function savePreferencesLocal(prefs: Preferences) {
  localStorage.setItem("prefs", JSON.stringify(prefs));
}

export async function putPreferences(prefs: Preferences): Promise<void> {
  const res = await fetch(`${API_BASE}/api/preferences`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "X-Client-Id": getClientId()
    },
    body: JSON.stringify(prefs),
  });
  if (!res.ok) {
    const t = await res.text();
    throw new Error(t || "Failed to save preferences");
  }
}

export async function postTranslate(text: string): Promise<TranslateResponse> {
  const res = await fetch(`${API_BASE}/api/translate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Client-Id": getClientId()
    },
    body: JSON.stringify({ text }),
  });
  const json = await res.json().catch(() => null);
  if (!res.ok) {
    throw new Error((json && json.detail) ? json.detail : "Translate failed");
  }
  return json as TranslateResponse;
}
