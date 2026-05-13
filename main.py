import streamlit as st
import google.generativeai as genai
import requests
import pandas as pd
from datetime import datetime

# --- CONFIG & ASSETS ---
st.set_page_config(page_title="Vantage Hub Pro", page_icon="⚡", layout="wide")

# --- CUSTOM CSS (The "Pro" Look) ---
st.markdown("""
    <style>
    .main { background-color: #080a0f; }
    .stMetric { border: 1px solid #1f2937; padding: 20px; border-radius: 12px; background: #111827; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1f2937; border-radius: 8px 8px 0 0; padding: 10px 20px; color: white;
    }
    .stTabs [aria-selected="true"] { background-color: #3b82f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (Memory) ---
if "research_history" not in st.session_state:
    st.session_state.research_history = []

# --- APP LAYOUT ---
st.title("⚡ Vantage Hub Pro")
st.caption(f"System Active | {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Top Level Tabs for a cleaner feel
tab_market, tab_research, tab_code = st.tabs(["📊 Market Terminal", "🧠 Research Lab", "🛠️ Code Architect"])

# --- TAB 1: MARKET TERMINAL ---
with tab_market:
    col_input, col_news = st.columns([1, 3])
    
    with col_input:
        st.subheader("Watchlist")
        symbol = st.text_input("Ticker Symbol", "BTC").upper()
        if st.button("Refresh Data", use_container_width=True):
            # (API Logic remains the same, but display is improved)
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={st.secrets['FINNHUB_API_KEY']}"
            data = requests.get(url).json()
            if 'c' in data:
                st.metric("Price", f"${data['c']:,.2f}", f"{data['d']:+}")
                st.progress(abs(data['dp']/100) if data['dp'] else 0)
    
    with col_news:
        st.subheader(f"Live Insights: {symbol}")
        # AI-generated market sentiment
        if st.button(f"Analyze Sentiment for {symbol}"):
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Give a 3-bullet point summary of current market sentiment for {symbol} as of May 2026.")
            st.info(response.text)

# --- TAB 2: RESEARCH LAB ---
with tab_research:
    query = st.chat_input("Enter research topic...")
    if query:
        st.session_state.research_history.append(f"User: {query}")
        with st.spinner("Compiling Intelligence..."):
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(query)
            st.session_state.research_history.append(f"AI: {response.text}")
            
    for msg in st.session_state.research_history:
        st.write(msg)

# --- TAB 3: CODE ARCHITECT ---
with tab_code:
    st.subheader("Build & Deploy")
    code_req = st.text_area("Describe the logic...")
    if st.button("Generate Snippet"):
        # Code generation logic...
        st.code("print('New logic pending...')", language='python')