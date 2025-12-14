import os
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from langchain_core.pydantic_v1 import BaseModel, Field  
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
llm = llm.configurable_fields(max_tokens=ConfigurableField(id='max_tokens'))

ROLES = {
    "1": {
        "name": "日本語の翻訳者",
        "description": "日本語に翻訳できる専門家",
        "details": "あなたは熟練した翻訳者です。文脈とニュアンスを考慮して、正確で自然な翻訳を提供してください。"
    },
    "2": {
        "name": "中文翻译者",
        "description": "可以翻译成中文的专家",
        "details": "您是一位经验丰富的翻译者。请考虑上下文和细微差别，提供准确自然的翻译。"
    },
    "3": {
        "name": "English translator",
        "description": "An expert who can translate into English",
        "details": "You are an experienced translator. Please consider the context and nuances to provide an accurate and natural translation."
    }
}

class TranslatorAgent(BaseModel):
    text: str = Field(..., description="The text to be translated")

# The following code has been commented out as it is no longer needed with the new implementation using LangChain and ChatOpenAI.
# def detect_language(text):

#     has_japanese = False
#     has_chinese = False
#     has_english = False
    
#     for char in text:
#         # \u3040-\u309F: Hiragana, \u30A0-\u30FF: Katakana
#         if '\u3040' <= char <= '\u30FF':
#             has_japanese = True
#             break # if we found Japanese characters, we can stop checking further
        
#         # \u4e00-\u9FFF: CJK Unified Ideographs,since Chinese and Japanese share many characters, we need to check this after Japanese 
#         elif '\u4e00' <= char <= '\u9FFF':
#             has_chinese = True
            
#         # \u0041-\u005A: A-Z, \u0061-\u007A: a-z
#         elif '\u0041' <= char <= '\u005A' or '\u0061' <= char <= '\u007A':
#             has_english = True

#     if has_japanese:
#         detected_lang = 'Japanese'
#     elif has_chinese:
#         detected_lang = 'Chinese'
#     elif has_english:
#         detected_lang = 'English'
#     else:
#         return []

#     return detected_lang

# def translate(text):#you can also change the language to other languages
#     lang = detect_language(text)

#     if not lang:
#         print("No texts, 文章がありません, 没有文本")
#         return
#     # Determine target languages
#     all_langs = {"Chinese", "Japanese", "English"}
#     all_langs.remove(lang)
#     target_lang_1, target_lang_2 = list(all_langs)

#     # Prepare the prompt for translation
#     prompt = f"""
#     Please act as an expert translator. Translate the following source text into two target languages.
#     Provide the output in the exact format below, without any additional notes or explanations.

#     Source Language: {lang}
#     Source Text: "{text}"

#     {target_lang_1}:
#     {target_lang_2}:
#     """

#     completion = client.chat.completions.create(
#     model="qwen-plus", 
#     messages=[{"role": "user", "content": prompt}]
# )
#     print(completion.choices[0].message.content)

# if __name__ == "__main__":
#     print("3 Language Translator(enter 'q' to quit)\n")
#     while True:
#         user_input = input("\nEnter text to translate:\n")
#         if user_input.strip().lower() == 'q':
#             break
#         translate(user_input)