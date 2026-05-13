import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
from PIL import Image

# --- 1. SETTINGS & AI CONFIG ---
st.set_page_config(page_title="Vantage AI", layout="wide", initial_sidebar_state="expanded")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. THE "ELITE" CSS (Gemini Clone) ---
st.markdown("""
    <style>
    /* Gemini Colors & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&display=swap');
    
    .stApp { background-color: #131314; color: #e3e3e3; font-family: 'Google Sans', sans-serif; }
    
    /* Sidebar Navigation Overhaul */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #3c4043;
        padding-top: 2rem;
    }
    
    /* Modern Chat Bubbles */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        margin-bottom: 20px !important;
    }

    /* Professional Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent; border: 1px solid #3c4043;
        border-radius: 20px; padding: 6px 20px; color: #9aa0a6;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3c4043 !important; color: white !important;
        border: 1px solid #8ab4f8 !important;
    }

    /* Hide default Streamlit clutter */
    header, footer, #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE HAMBURGER SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #8ab4f8; margin-bottom: 20px;'>Vantage Hub</h2>", unsafe_allow_html=True)
    page = st.radio("Navigation", ["🔍 Research Lab", "💻 Code Architect", "📈 Crypto Market"], label_visibility="collapsed")
    st.divider()
    
    st.subheader("📁 Analysis Tools")
    uploaded_file = st.file_uploader("Upload Image/Chart", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

# --- 4. PAGE: RESEARCH LAB ---
if page == "🔍 Research Lab":
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>How can I help you today?</h1>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Enter a prompt here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner(" "):
                content = [prompt, Image.open(uploaded_file)] if uploaded_file else prompt
                response = model.generate_content(content)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- 5. PAGE: CRYPTO MARKET (Multi-Tabbed Hub) ---
elif page == "📈 Crypto Market":
    st.title("Asset Intelligence Terminal")
    
    # Sub-tabs for the specific markets you requested
    market_tabs = st.tabs(["💎 Major Crypto", "🚀 Meme Coins", "🛡️ Gold & Silver", "🔮 Up & Coming"])
    
    with market_tabs[0]:
        st.subheader("Bitcoin & Ethereum Live")
        components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=60&theme=dark" width="100%" height="500"></iframe>', height=500)
    
    with market_tabs[1]:
        st.subheader("Meme Coin Scalper")
        meme = st.selectbox("Select Token", ["PEPEUSDT", "DOGEUSDT", "SHIBUSDT", "BONKUSDT"])
        components.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:{meme}&interval=5&theme=dark" width="100%" height="400"></iframe>', height=400)
    
    with market_tabs[2]:
        col_g, col_s = st.columns(2)
        with col_g:
            st.caption("Gold Spot Price")
            components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=TVC:GOLD&interval=D&theme=dark" width="100%" height="350"></iframe>', height=350)
        with col_s:
            st.caption("Silver Spot Price")
            components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=TVC:SILVER&interval=D&theme=dark" width="100%" height="350"></iframe>', height=350)

    with market_tabs[3]:
        st.subheader("AI Trend Prediction")
        if st.button("Analyze Up & Coming Moonshots"):
            with st.spinner("Scanning DEX liquidity..."):
                analysis = model.generate_content("Identify 3 crypto tokens with high community growth and low market cap for May 2026. Focus on Solana and Base networks.")
                st.write(analysis.text)

# --- 6. PAGE: CODE ARCHITECT ---
elif page == "💻 Code Architect":
    st.title("Code Architect")
    task = st.text_area("What are we building?", placeholder="e.g., A Python script for technical analysis...", height=200)
    if st.button("Generate Code"):
        with st.spinner(" "):
            res = model.generate_content(f"Write high-quality, professional code for: {task}")
            st.code(res.text, language='python')