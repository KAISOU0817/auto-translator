-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- User preferences (keyed by client_id; swap to real user id later)
CREATE TABLE IF NOT EXISTS user_prefs (
  client_id TEXT PRIMARY KEY,
  native_lang TEXT NOT NULL,
  target_langs TEXT[] NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Dictionary entries
-- pair: "native-target" e.g. zh-en, zh-ja
-- headword: word in target language
-- definition_native: meaning/definition in native language
-- embedding: optional; for true RAG / semantic lookup
CREATE TABLE IF NOT EXISTS dict_entries (
  id BIGSERIAL PRIMARY KEY,
  pair TEXT NOT NULL,
  headword TEXT NOT NULL,
  definition_native TEXT NOT NULL,
  extra JSONB,
  embedding VECTOR(1536),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_dict_entries_pair_headword
  ON dict_entries (pair, headword);

-- Optional vector index (only useful once you store embeddings)
-- CREATE INDEX IF NOT EXISTS idx_dict_entries_embedding
--   ON dict_entries USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Sample data (remove in real usage)
INSERT INTO dict_entries (pair, headword, definition_native, extra)
VALUES
  ('zh-en', 'convenient', '方便的；便利的', '{"pos":"adj"}'),
  ('zh-en', 'reservation', '预约；预订', '{"pos":"n"}'),
  ('zh-ja', '予約', '预约；预订', '{"reading":"よやく","pos":"名詞"}'),
  ('zh-ja', '便利', '方便；便利', '{"reading":"べんり","pos":"形容動詞"}')
ON CONFLICT DO NOTHING;
