import os
from openai import OpenAI

client = OpenAI(
    api_key="Add your API key here", #Please add your API key in " "
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"#In this case, I use Qwen's API
)

def detect_language(text):
    # Simple judgment whether it contains Japanese characters
    for ch in text:
        if '\u3040' <= ch <= '\u30ff':
            return 'ja'
    return 'zh'

def translate(text):#you can also change the language to other languages
    lang = detect_language(text)
    target = "中文" if lang == "ja" else "日语"
    prompt = f"请将以下文本翻译为{target}:\n{text}"

    # 

    completion = client.chat.completions.create(
    model="qwen-plus", 
    messages=[{"role": "user", "content": prompt}]
)
    print(completion.choices[0].message.content)

if __name__ == "__main__":
    print("中日互译翻译器（输入 q 退出）")
    while True:
        user_input = input("\n请输入中文或日语:\n")
        if user_input.strip().lower() == 'q':
            break
        translate(user_input)