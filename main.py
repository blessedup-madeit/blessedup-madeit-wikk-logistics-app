import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
from PIL import Image
from datetime import datetime

# --- 1. SYSTEM & BRANDING ---
st.set_page_config(page_title="Vantage AI Elite", page_icon="♊", layout="wide", initial_sidebar_state="collapsed")

# Core Engine
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. THE 2026 GLASSMORPHISM STYLE ---
st.markdown("""
    <style>
    /* Dark Base */
    .main { background-color: #080808; color: #e3e3e3; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #333; }
    
    /* Frosted Glass Chat Bubbles */
    .stChatMessage { 
        background: rgba(255, 255, 255, 0.03) !important; 
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px;
        margin-bottom: 12px;
    }
    
    /* Professional Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: transparent; border: 1px solid #444; border-radius: 8px; 
        padding: 8px 25px; color: #aaa; transition: 0.3s;
    }
    .stTabs [aria-selected="true"] { border-color: #3b82f6 !important; color: white !important; background: rgba(59, 130, 246, 0.1) !important; }
    
    /* Animation for the AI "Thinking" state */
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
    .thinking { animation: pulse 1.5s infinite; color: #3b82f6; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR NAVIGATION (Hamburger Menu) ---
with st.sidebar:
    st.title("♊ Vantage Elite")
    st.caption("Advanced Intelligence Hub v4.0")
    st.divider()
    page = st.radio("Navigation", ["🔍 Research Lab", "💻 Code Architect", "📈 Terminal"], label_visibility="collapsed")
    st.divider()
    
    st.subheader("📸 Visual Analysis")
    uploaded_file = st.file_uploader("Drop charts/images here", type=['png', 'jpg', 'jpeg'])
    if uploaded_file:
        st.image(uploaded_file, caption="Scan Ready", use_container_width=True)
    
    if st.button("Reset Session", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- 4. PAGE LOGIC ---

# PAGE: RESEARCH (The Gemini UI Clone)
if page == "🔍 Research Lab":
    st.title("Research Intelligence")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask Vantage anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.status("Vantage is processing...", expanded=True) as status:
                st.write("Searching database...")
                st.write("Synthesizing context...")
                content = [prompt, Image.open(uploaded_file)] if uploaded_file else prompt
                response = model.generate_content(content)
                status.update(label="Analysis Complete", state="complete", expanded=False)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# PAGE: ASSET TERMINAL (TradingView & Assets)
elif page == "📈 Terminal":
    st.title("Elite Asset Terminal")
    
    # Sub-Navigation Tabs
    t1, t2, t3 = st.tabs(["💎 Crypto Majors", "🚀 Meme Moonshots", "🛡️ Metals & Commodities"])
    
    with t1:
        st.subheader("Bitcoin / Ethereum Live Stream")
        components.html("""
            <div style="height:550px;"><iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=60&theme=dark" width="100%" height="550"></iframe></div>
        """, height=550)
        
    with t2:
        st.subheader("Meme Coin Sentiment & Scalping")
        m_col1, m_col2 = st.columns([2, 1])
        with m_col1:
            meme = st.selectbox("Select Target", ["PEPEUSDT", "DOGEUSDT", "SHIBUSDT", "BONKUSDT"])
            components.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:{meme}&interval=5&theme=dark" width="100%" height="450"></iframe>', height=450)
        with m_col2:
            st.markdown("### AI Moonshot Scan")
            if st.button("Generate Signal"):
                with st.spinner("Scanning social volume & DEX liquidity..."):
                    sig = model.generate_content(f"Give a professional day-trading signal for {meme} based on current high-volatility patterns.")
                    st.success(sig.text)

    with t3:
        st.subheader("Precious Metals & Indices")
        col_gold, col_silver = st.columns(2)
        with col_gold:
            st.caption("GOLD / USD SPOT")
            components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=TVC:GOLD&interval=D&theme=dark" width="100%" height="350"></iframe>', height=350)
        with col_silver:
            st.caption("SILVER / USD SPOT")
            components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=TVC:SILVER&interval=D&theme=dark" width="100%" height="350"></iframe>', height=350)

# PAGE: CODING
elif page == "💻 Code Architect":
    st.title("Code Architect")
    code_task = st.text_area("What are we building?", placeholder="Define your logic or script...")
    if st.button("Build Project"):
        with st.status("Architecting logic..."):
            res = model.generate_content(f"Write clean, professional code for: {code_task}")
        st.code(res.text, language='python')