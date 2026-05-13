import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
from PIL import Image

# --- 1. CONFIG & PREMIUM CSS (THE "GEMINI" LOOK) ---
st.set_page_config(page_title="Gemini Vantage", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Dark Background & Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500&display=swap');
    .stApp { background-color: #131314; color: #e3e3e3; font-family: 'Google Sans', sans-serif; }
    
    /* Transparent Sidebar */
    [data-testid="stSidebar"] { background-color: #1e1f20 !important; border-right: 1px solid #3c4043; }
    
    /* Glassmorphism Chat Bubbles */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        margin-bottom: 20px !important;
    }

    /* Professional Tab Buttons */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 50px; border: 1px solid #3c4043; padding: 6px 20px; color: #9aa0a6;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3c4043 !important; color: white !important; border: 1px solid #8ab4f8 !important;
    }
    header, footer, #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI SETUP WITH WEB GROUNDING ---
# Ensure your key is in Streamlit Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# We use the Google Search Retrieval tool to get reliable web sources
tools = [{"google_search_retrieval": {}}] 
model = genai.GenerativeModel('gemini-1.5-flash', tools=tools)

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#8ab4f8'>♊ Gemini Vantage</h2>", unsafe_allow_html=True)
    page = st.radio("Navigation", ["🔍 Intelligence Hub", "💻 Code Architect", "📈 Market Terminal"], label_visibility="collapsed")
    st.divider()
    st.caption("May 2026 Stable Build")

# --- 4. TAB 1: INTELLIGENCE HUB (WEB SEARCH + CITATIONS) ---
if page == "🔍 Intelligence Hub":
    st.markdown("<h1 style='text-align: center; margin-top: 50px;'>How can I help you today?</h1>", unsafe_allow_html=True)
    
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question (Web Grounded)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Searching reliable web sources..."):
                # The model uses the google_search_retrieval tool here
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- 5. TAB 2: CODE ARCHITECT ---
elif page == "💻 Code Architect":
    st.title("Code Architect")
    task = st.text_area("Describe the code you need built...", height=200)
    if st.button("Generate Professional Script"):
        with st.spinner("Writing clean code..."):
            code_res = model.generate_content(f"Write professional, optimized code for: {task}")
            st.code(code_res.text)

# --- 6. TAB 3: MARKET TERMINAL (REAL-TIME SCREENERS) ---
elif page == "📈 Market Terminal":
    st.title("Global Market Intel")
    
    # Sub-Tabs as requested
    m_tabs = st.tabs(["💎 Major Crypto", "🚀 All Meme Coins", "🛠️ Advanced Filter Screener"])
    
    with m_tabs[0]:
        st.subheader("Major Assets (Real-Time)")
        components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&theme=dark" width="100%" height="500"></iframe>', height=500)
    
    with m_tabs[1]:
        st.subheader("Meme Coin Radar")
        st.caption("Active meme tokens on Binance/Global markets.")
        ticker = st.selectbox("Select Ticker", ["PEPEUSDT", "DOGEUSDT", "SHIBUSDT", "BONKUSDT", "FLOKIUSDT"])
        components.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:{ticker}&theme=dark" width="100%" height="450"></iframe>', height=450)

    with m_tabs[2]:
        st.subheader("Global Crypto Screener")
        st.info("Sort by Popularity, Price, or Growth using the 'Filters' button inside the widget below.")
        # This widget includes the filtering system for ALL crypto/memes
        components.html("""
            <div class="tradingview-widget-container">
              <iframe src="https://www.tradingview-widgets.com/embed-widget/crypto-mkt-screener/?customer=binance&theme=dark" width="100%" height="600" frameborder="0"></iframe>
            </div>
        """, height=620)