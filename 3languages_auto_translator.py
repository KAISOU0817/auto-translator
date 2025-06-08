import os
from openai import OpenAI

client = OpenAI(
    api_key="Add your API key here", #Please add your API key in " "
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"#In this case, I use Qwen's API
)

def detect_language(text):

    has_japanese = False
    has_chinese = False
    has_english = False
    
    for char in text:
        # \u3040-\u309F: Hiragana, \u30A0-\u30FF: Katakana
        if '\u3040' <= char <= '\u30FF':
            has_japanese = True
            break # if we found Japanese characters, we can stop checking further
        
        # \u4e00-\u9FFF: CJK Unified Ideographs,since Chinese and Japanese share many characters, we need to check this after Japanese 
        elif '\u4e00' <= char <= '\u9FFF':
            has_chinese = True
            
        # \u0041-\u005A: A-Z, \u0061-\u007A: a-z
        elif '\u0041' <= char <= '\u005A' or '\u0061' <= char <= '\u007A':
            has_english = True

    if has_japanese:
        detected_lang = 'Japanese'
    elif has_chinese:
        detected_lang = 'Chinese'
    elif has_english:
        detected_lang = 'English'
    else:
        return []

    return detected_lang

def translate(text):#you can also change the language to other languages
    lang = detect_language(text)
    if not lang:
        print("No texts, 文章がありません, 没有文本")
        return
    # Determine target languages
    if lang == 'Japanese':
        target = "Chinese and English"
    elif lang == 'Chinese':
        target = "Japanese and English"
    else:
        target = "Chinese and Japanese" 

    # Prepare the prompt for translation
    prompt = f"translate the following {lang} text to {target}:\n{text}\n\n" 

    completion = client.chat.completions.create(
    model="qwen-plus", 
    messages=[{"role": "user", "content": prompt}]
)
    print(completion.choices[0].message.content)

if __name__ == "__main__":
    print("3 Language Translator(enter 'q' to quit)\n")
    while True:
        user_input = input("\nEnter text to translate:\n")
        if user_input.strip().lower() == 'q':
            break
        translate(user_input)