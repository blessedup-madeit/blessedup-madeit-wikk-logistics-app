import streamlit as st
import google.generativeai as genai
import requests
import pandas as pd

# --- API SETUP ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    FINNHUB_KEY = st.secrets["FINNHUB_API_KEY"]
except Exception as e:
    st.error("API Keys missing in Streamlit Secrets! Please add them to continue.")
    st.stop()

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Vantage Hub", 
    page_icon="🌐",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PROFESSIONAL FINISH ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #00ffcc; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #262730; color: white; border: 1px solid #4a4a4a; }
    .stButton>button:hover { border: 1px solid #00ffcc; color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🌐 Vantage Hub")
    st.markdown("*Your Personal Command Center*")
    st.divider()
    
    mode = st.radio(
        "Select Workflow:",
        ["Research Lab", "Code Architect", "Market Terminal"],
        index=0
    )
    
    st.divider()
    st.caption("v2.0 | Powered by Gemini Pro")

# --- MODE 1: RESEARCH LAB ---
if mode == "Research Lab":
    st.header("🔬 Research Lab")
    st.subheader("Deep-Dive Intelligence")
    
    query = st.text_area("What would you like to investigate today?", placeholder="Describe your topic in detail...")
    
    col1, col2 = st.columns([2, 1])
    with col2:
        detail_level = st.select_slider("Depth of Research:", options=["Executive Summary", "Standard", "Comprehensive"])
    
    if st.button("Initialize Research"):
        if query:
            with st.spinner("Scanning databases and generating report..."):
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Act as a professional researcher. Provide a {detail_level} report on: {query}. Use clear headers, bullet points, and a concluding summary."
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
        else:
            st.warning("Please enter a research topic to begin.")

# --- MODE 2: CODE ARCHITECT ---
elif mode == "Code Architect":
    st.header("💻 Code Architect")
    st.subheader("Automated Development")
    
    code_query = st.text_area("Describe the script or function you need:", placeholder="e.g. Build a Python script to automate file organization...")
    
    c1, c2 = st.columns(2)
    with c1:
        language = st.selectbox("Language:", ["Python", "JavaScript", "HTML/CSS", "SQL", "C#", "Go"])
    with c2:
        style = st.selectbox("Coding Style:", ["Functional", "Object-Oriented", "Beginner-Friendly"])

    if st.button("Generate Architecture"):
        if code_query:
            with st.spinner(f"Architecting {language} code..."):
                model = genai.GenerativeModel('gemini-pro')
                prompt = f"Act as a Senior Software Engineer. Language: {language}. Style: {style}. Task: {code_query}. Provide clean code with comments explaining each part."
                response = model.generate_content(prompt)
                st.code(response.text, language=language.lower())
        else:
            st.warning("Please describe your project.")

# --- MODE 3: MARKET TERMINAL ---
elif mode == "Market Terminal":
    st.header("📈 Market Terminal")
    st.subheader("Real-Time Financial Data")
    
    symbol = st.text_input("Enter Ticker Symbol (e.g., AAPL, BTC, ETH, TSLA):", "BTC").upper()
    
    if st.button("Fetch Market Data"):
        with st.spinner(f"Fetching data for {symbol}..."):
            url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}"
            try:
                data = requests.get(url).json()
                
                if data and 'c' in data and data['c'] != 0:
                    # Professional Dashboard View
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Current", f"${data['c']:,.2f}", f"{data['d']:+}")
                    m2.metric("High", f"${data['h']:,.2f}")
                    m3.metric("Low", f"${data['l']:,.2f}")
                    m4.metric("Open", f"${data['o']:,.2f}")
                    
                    st.divider()
                    st.info(f"Currently viewing live data for **{symbol}**. Data updated via Finnhub API.")
                else:
                    st.error(f"Symbol '{symbol}' not found. Note: For Crypto, try symbols like BTC or ETH.")
            except Exception as e:
                st.error("Connection error. Please check your Finnhub API key.")