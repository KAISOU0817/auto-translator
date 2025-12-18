import React from "react";

export const metadata = {
  title: "Translator + Vocab Agent",
  description: "LangGraph-based translator with vocabulary extraction + dictionary lookup"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh">
      <body style={{ margin: 0, fontFamily: "ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto" }}>
        {children}
      </body>
    </html>
  );
}
