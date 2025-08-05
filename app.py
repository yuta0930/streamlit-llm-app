from dotenv import load_dotenv
import os

load_dotenv()  # .envファイルから環境変数を読み込む

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# OpenAIのAPIキーを取得
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY が .env に設定されていません。")

# アプリの概要・操作説明
st.markdown("""
## アプリ概要
このアプリは、LangChainとOpenAIの言語モデルを利用したチャットデモです。  
「料理の専門家」または「トレーニングの専門家」として、質問に対して専門的な回答を得ることができます。

### 操作方法
1. 上部のラジオボタンで専門家の種類を選択してください。
2. 下の入力欄に質問を入力し、Enterキーを押してください。
3. 選択した専門家が質問に回答します。
""")

# LLMからの回答を取得する関数
def get_llm_response(user_input: str, expert_type: str) -> str:
    if expert_type.startswith("A"):
        system_prompt = "あなたは料理の領域の専門家です。ユーザーの質問には料理の専門家として答えてください。"
    else:
        system_prompt = "あなたはトレーニングの領域の専門家です。ユーザーの質問にはトレーニングの専門家として答えてください。"
    
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_input)
    ]
    
    response = llm(messages)
    return response.content

# Streamlitタイトル
st.title("LangChain LLM チャットデモ")

# 専門家の種類を選択
expert_type = st.radio(
    "専門家の種類を選択してください:",
    ("A: 料理の専門家", "B: トレーニングの専門家")
)

# ユーザー入力フォーム
user_input = st.text_input("質問を入力してください:")

# 入力がある場合にLLMへ送信して返答を表示
if user_input:
    with st.spinner("考え中..."):
        answer = get_llm_response(user_input, expert_type)
        st.write("### 回答:")
        st.success(answer)