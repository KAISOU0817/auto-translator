# zh-ja-translator

A minimal, powerful, and intelligent command-line translator between Chinese and Japanese, powered by Large Language Models (LLMs) such as OpenAI GPT or Qwen via OpenAI-compatible APIs.

---

## 🌟 Why This Project?

Most translation tools—Google Translate, DeepL, and even system-level translators—require you to manually select source and target languages. For people who switch frequently between only two languages (in this case, **Chinese** and **Japanese**), this is surprisingly inefficient.

### ✨ Key Benefits:
- **Smart Auto-Detection**: No need to specify the input language. Just paste your sentence in either Chinese or Japanese, and it gets translated to the other automatically.
- **Powered by LLMs**: Unlike traditional rule-based or statistical translators, this tool uses LLMs to generate more **natural**, **context-aware**, and **fluent** translations.
- **Minimal Interface**: Just run it, type or paste your sentence, and get your result. No UI clutter, no dropdown lists.

---

## 📦 Features

- 🔁 Chinese ↔ Japanese translation only (you can also chose two languages you offen use!)
- 🧠 Automatic language detection
- 🚀 LLM backend: configurable to OpenAI, DeepSeek, Qwen, or any OpenAI-compatible model
- 💻 Simple Python CLI tool (GUI version coming soon!)

---

## 🛠️ Installation

First, make sure you have Python 3.7+ installed. Then:

```bash
pip install openai
```


## 🚀 Usage

```bash
python zh_ja_translator.py
```

## Sample
请输入中文或日语:
我想去日本旅行。
翻译结果：
日本に旅行に行きたいです。


## Why Not Use Google Translate?
- Too many clicks: Selecting languages manually every time gets tedious.
- Lower-quality output: LLMs often produce translations with better context handling and more native phrasing.
- No customization: With LLMs, you can easily fine-tune the prompt for tone, formality, or purpose.

## Future Plans
- GUI version using Tkinter or PyQt
- Save translation history
- Batch translation
- Voice input / speech-to-text
-Web version with Streamlit or Flask


