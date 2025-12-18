export type Preferences = {
  native_lang: string;
  target_langs: [string, string];
};

export type VocabItem = {
  word: string;
  reason?: string | null;
  meaning_native?: string | null;
  extra?: any;
  found?: boolean;
};

export type TranslateResponse = {
  translations: Record<string, string>;
  vocab: Record<string, VocabItem[]>;
};
