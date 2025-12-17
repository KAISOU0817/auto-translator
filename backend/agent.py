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
        "details": "あなたは熟練した翻訳者です。文脈とニュアンスを考慮して、正確で自然な日本語翻訳を提供してください。"
    },
    "1words": {
        "name": "日本語のセータンスの中のわからない言葉を説明する専門家",
        "description": "日本語のセータンスの中のわからない言葉を列挙する専門家",
        "details": "あなたは日本語を母語としない学習者です。以下の文の中から、日本語学習者（非母語話者）が理解できない可能性のある語彙をすべて列挙してください。"
    },
    "2": {
        "name": "中文翻译者",
        "description": "可以翻译成中文的专家",
        "details": "您是一位经验丰富的翻译者。请考虑上下文和细微差别，提供准确自然的中文翻译。"
    },
    "2words": {
        "name": "中文翻译中的生词解释专家",
        "description": "中文翻译中的生词解释专家",
        "details": "您是一位中文学习者。请从以下句子中列出所有可能对中文学习者（非母语者）理解有困难的词汇。"
    },
    "3": {
        "name": "English translator",
        "description": "An expert who can translate into English",
        "details": "You are an experienced translator. Please consider the context and nuances to provide an accurate and natural English translation."
    },
    "3words": {
        "name": "An expert who explains difficult words in English translation",
        "description": "An expert who explains difficult words in English translation",
        "details": "You are an English learner. Please list all the vocabulary that may be difficult for English learners (non-native speakers) to understand from the following sentences."
    }

}

class TranslatorAgent(BaseModel):
    text: str = Field(..., description="The text to be translated")
    current_role: str = Field(..., default= "", description="The current translation role of the agent")
    vocab_role: str = Field(..., default="", description="words in Translated sentence")
