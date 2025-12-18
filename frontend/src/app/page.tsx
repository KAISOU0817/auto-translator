"use client";

import React, { useEffect, useState } from "react";
import PreferencesModal from "../components/PreferencesModal";
import ResultPanel from "../components/ResultPanel";
import { getSavedPreferences, putPreferences, savePreferencesLocal, postTranslate } from "../lib/api";
import { Preferences, TranslateResponse } from "../lib/types";

export default function Page() {
  const [prefs, setPrefs] = useState<Preferences | null>(null);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [data, setData] = useState<TranslateResponse | null>(null);

  useEffect(() => {
    const p = getSavedPreferences();
    setPrefs(p);
  }, []);

  const openPrefs = !prefs;

  return (
    <div style={styles.page}>
      <PreferencesModal
        open={openPrefs}
        onSave={async (p) => {
          await putPreferences(p);
          savePreferencesLocal(p);
          setPrefs(p);
        }}
      />

      <header style={styles.header}>
        <h1 style={{ margin: 0 }}>翻译 + 生词（LangGraph）</h1>
        <div style={{ opacity: 0.8, marginTop: 6 }}>
          {prefs ? (
            <span>
              母语：<b>{prefs.native_lang}</b> ｜ 目标：<b>{prefs.target_langs[0]}</b> + <b>{prefs.target_langs[1]}</b>
            </span>
          ) : (
            <span>请先设置语言偏好</span>
          )}
          <button
            style={styles.linkBtn}
            onClick={() => setPrefs(null)}
            title="重新设置（会重新弹出设置框）"
          >
            重新设置
          </button>
        </div>
      </header>

      <main style={styles.main}>
        <textarea
          style={styles.textarea}
          placeholder="输入中文（或任意语言）。系统会根据你的偏好翻译到两种目标语言，并提取生词。"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <div style={{ display: "flex", gap: 10, marginTop: 10, alignItems: "center" }}>
          <button
            style={styles.button}
            disabled={!prefs || !text.trim() || loading}
            onClick={async () => {
              setErr(null);
              setData(null);
              setLoading(true);
              try {
                const res = await postTranslate(text);
                setData(res);
              } catch (e: any) {
                setErr(e?.message ?? "请求失败");
              } finally {
                setLoading(false);
              }
            }}
          >
            {loading ? "处理中..." : "开始"}
          </button>

          {err && <div style={{ color: "#b00020" }}>{err}</div>}
        </div>

        {data && <ResultPanel data={data} />}
      </main>

      <footer style={{ opacity: 0.7, marginTop: 24 }}>
        <small>
          提示：词典未命中的单词会显示“词典未命中”，你可以往 Postgres 的 dict_entries 表里补充词条。
        </small>
      </footer>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  page: {
    minHeight: "100vh",
    background: "#fafafa",
    padding: 18,
  },
  header: {
    maxWidth: 980,
    margin: "0 auto",
    marginTop: 8,
  },
  main: {
    maxWidth: 980,
    margin: "0 auto",
    marginTop: 14,
  },
  textarea: {
    width: "100%",
    minHeight: 140,
    borderRadius: 12,
    border: "1px solid #ddd",
    padding: 14,
    fontSize: 16,
    outline: "none",
    resize: "vertical",
  },
  button: {
    padding: "10px 14px",
    borderRadius: 10,
    border: "1px solid #111",
    background: "#111",
    color: "white",
    cursor: "pointer",
  },
  linkBtn: {
    marginLeft: 10,
    background: "transparent",
    border: "none",
    color: "#0b57d0",
    cursor: "pointer",
    textDecoration: "underline",
    padding: 0,
  },
};
