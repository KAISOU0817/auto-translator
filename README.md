# auto-translator

A minimal, powerful, and intelligent translator between English, Chinese and Japanese, powered by Large Language Models (LLMs) such as OpenAI GPT via OpenAI-compatible APIs.

---

## Why This Project?

Conventional translation software and websites, while powerful, present a user experience flaw: they offer a vast selection of languages but require manual selection for every translation. This process is surprisingly inefficient for the average user. According to a UNESCO report, fewer than **3%** of the world's population speaks four or more languages, which means the vast majority of people operate within a small set of two or three.

This data reflects my own experience as an international student in Japan, where I constantly switch between **Chinese, English, and Japanese**. My daily needs vary widely: translating my thoughts from Chinese to Japanese for assignments, looking up unfamiliar English words in Chinese while reading, or finding the original English source for a Japanese word written in Katakana. The repetitive, manual task of setting the source and target languages for each of these simple queries became a significant point of friction.

To address this inefficiency, I developed this tool. It automatically detects the input language among the three and intelligently translates it into one of the other two, creating a seamless and efficient workflow for multilingual users like myself.



###  Key Benefits:
- **Smart Auto-Detection**: No need to specify the input language. Just paste your sentence in either Chinese or Japanese, and it gets translated to the other automatically.
- **Powered by LLMs**: Unlike traditional rule-based or statistical translators, this tool uses LLMs to generate more **natural**, **context-aware**, and **fluent** translations.
- **Minimal Interface**: Just run it, type or paste your sentence, and get your result. No UI clutter, no dropdown lists.

---

## Features

-  Chinese ↔ Japanese translation only (you can also chose two languages you offen use!)
-  Automatic language detection
-  LLM backend: configurable to OpenAI, DeepSeek, Qwen, or any OpenAI-compatible model
-  Simple Python CLI tool (GUI version coming soon!)

---




##  Usage

1. Copy env file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and set **OPENAI_API_KEY** (required for translation/vocab extraction).
3. Start:
   ```bash
   docker compose up --build
   ```
4. Open:
   - Frontend: http://localhost:3000
   - Backend docs: http://localhost:8000/docs

## Sample
Enter text to translate:
我想去日本旅行。

翻译结果：
日本に旅行に行きたいです。
I want to go on a trip to Japan.


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


