import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# --- APIキーの取得 ---
def get_api_key():
    # Cloud環境（Streamlit Community Cloud）では secrets.toml から取得
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    
    # ローカル環境では .env から取得
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        st.error("APIキーが設定されていません。secrets または .env を確認してください。")
        st.stop()
    return api_key

api_key = get_api_key()

# --- Streamlit UI ---
st.title("LangChain LLM チャットデモ")

st.markdown("""
## アプリ概要
このアプリは、LangChainとOpenAIの言語モデルを利用したチャットデモです。  
「料理の専門家」または「トレーニングの専門家」として、質問に対して専門的な回答を得ることができます。
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

# --- 入力欄 ---
expert_type = st.radio("専門家の種類を選択してください:", ("A: 料理の専門家", "B: トレーニングの専門家"))
user_input = st.text_input("質問を入力してください:")

if user_input:
    with st.spinner("考え中..."):
        answer = get_llm_response(user_input, expert_type)
        st.write("### 回答:")
        st.success(answer)