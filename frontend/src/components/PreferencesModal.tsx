"use client";

import React, { useMemo, useState } from "react";
import { Preferences } from "../lib/types";

const LANGS: { code: string; label: string }[] = [
  { code: "zh", label: "中文 (zh)" },
  { code: "en", label: "English (en)" },
  { code: "ja", label: "日本語 (ja)" },
  { code: "ko", label: "한국어 (ko)" },
  { code: "fr", label: "Français (fr)" },
  { code: "de", label: "Deutsch (de)" },
  { code: "es", label: "Español (es)" }
];

export default function PreferencesModal(props: {
  open: boolean;
  onSave: (prefs: Preferences) => Promise<void>;
}) {
  const [nativeLang, setNativeLang] = useState("zh");
  const [t1, setT1] = useState("en");
  const [t2, setT2] = useState("ja");
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const canSave = useMemo(() => {
    return nativeLang !== t1 && nativeLang !== t2 && t1 !== t2;
  }, [nativeLang, t1, t2]);

  if (!props.open) return null;

  return (
    <div style={styles.backdrop}>
      <div style={styles.modal}>
        <h2 style={{ marginTop: 0 }}>设置语言偏好</h2>
        <p style={{ marginTop: 0, opacity: 0.8 }}>
          只需设置一次，之后会自动使用这套翻译/生词逻辑。
        </p>

        <label style={styles.label}>母语</label>
        <select style={styles.select} value={nativeLang} onChange={(e) => setNativeLang(e.target.value)}>
          {LANGS.map(l => <option key={l.code} value={l.code}>{l.label}</option>)}
        </select>

        <label style={styles.label}>目标语言 1</label>
        <select style={styles.select} value={t1} onChange={(e) => setT1(e.target.value)}>
          {LANGS.map(l => <option key={l.code} value={l.code}>{l.label}</option>)}
        </select>

        <label style={styles.label}>目标语言 2</label>
        <select style={styles.select} value={t2} onChange={(e) => setT2(e.target.value)}>
          {LANGS.map(l => <option key={l.code} value={l.code}>{l.label}</option>)}
        </select>

        {!canSave && (
          <div style={{ color: "#b00020", marginTop: 8 }}>
            母语不能与目标语言相同，且两个目标语言不能重复。
          </div>
        )}
        {err && <div style={{ color: "#b00020", marginTop: 8 }}>{err}</div>}

        <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 16 }}>
          <button
            style={styles.button}
            disabled={!canSave || saving}
            onClick={async () => {
              setErr(null);
              setSaving(true);
              try {
                await props.onSave({ native_lang: nativeLang, target_langs: [t1, t2] });
              } catch (e: any) {
                setErr(e?.message ?? "保存失败");
              } finally {
                setSaving(false);
              }
            }}
          >
            {saving ? "保存中..." : "保存"}
          </button>
        </div>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  backdrop: {
    position: "fixed",
    inset: 0,
    background: "rgba(0,0,0,0.4)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: 16,
    zIndex: 50,
  },
  modal: {
    width: "100%",
    maxWidth: 520,
    background: "white",
    borderRadius: 12,
    padding: 16,
    boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
  },
  label: {
    display: "block",
    marginTop: 12,
    marginBottom: 6,
    fontWeight: 600,
  },
  select: {
    width: "100%",
    padding: 10,
    borderRadius: 8,
    border: "1px solid #ddd",
  },
  button: {
    padding: "10px 14px",
    borderRadius: 10,
    border: "1px solid #111",
    background: "#111",
    color: "white",
    cursor: "pointer",
  },
};
