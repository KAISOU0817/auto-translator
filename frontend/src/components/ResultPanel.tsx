"use client";

import React from "react";
import { TranslateResponse } from "../lib/types";

export default function ResultPanel({ data }: { data: TranslateResponse }) {
  const langs = Object.keys(data.vocab || {});
  return (
    <div style={{ marginTop: 16 }}>
      {langs.map((lang) => (
        <div key={lang} style={styles.card}>
          <h3 style={{ marginTop: 0 }}>生词（{lang}）</h3>

          {/* Translation is available; show if you want */}
          {data.translations?.[lang] && (
            <details style={{ marginBottom: 10 }}>
              <summary style={{ cursor: "pointer" }}>查看翻译</summary>
              <div style={{ marginTop: 8, whiteSpace: "pre-wrap" }}>{data.translations[lang]}</div>
            </details>
          )}

          {(data.vocab?.[lang] || []).length === 0 ? (
            <div style={{ opacity: 0.8 }}>（没有提取到生词）</div>
          ) : (
            <ul style={{ paddingLeft: 18 }}>
              {data.vocab[lang].map((it, idx) => (
                <li key={idx} style={{ marginBottom: 10 }}>
                  <div style={{ fontWeight: 700 }}>{it.word}</div>
                  {it.meaning_native ? (
                    <div style={{ opacity: 0.9 }}>{it.meaning_native}</div>
                  ) : (
                    <div style={{ opacity: 0.6 }}>
                      {it.found ? "（无释义）" : "（词典未命中）"}
                    </div>
                  )}
                  {it.reason && <div style={{ opacity: 0.7 }}>理由：{it.reason}</div>}
                  {it.extra && typeof it.extra === "object" && (
                    <pre style={styles.pre}>{JSON.stringify(it.extra, null, 2)}</pre>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  card: {
    background: "white",
    border: "1px solid #eee",
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    boxShadow: "0 6px 14px rgba(0,0,0,0.06)",
  },
  pre: {
    background: "#f7f7f7",
    padding: 10,
    borderRadius: 10,
    overflowX: "auto",
    marginTop: 8,
  },
};
