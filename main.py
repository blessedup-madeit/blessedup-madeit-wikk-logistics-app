import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
from PIL import Image

# --- 1. CORE CONFIG (FORCING SIDEBAR OPEN) ---
st.set_page_config(
    page_title="Vantage Elite", 
    page_icon="♊", 
    layout="wide", 
    initial_sidebar_state="expanded"  # This forces the sidebar to be open on start
)

# Connect AI
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. CLEAN PROFESSIONAL CSS (REMOVED SIDEBAR BLOCKERS) ---
st.markdown("""
    <style>
    .stApp { background-color: #131314; color: #e3e3e3; font-family: 'sans-serif'; }
    
    /* Premium Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e1f20 !important;
        border-right: 1px solid #3c4043;
    }
    
    /* Clean Chat Design */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    /* Fixed Top Nav (Backup Navigation) */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DUAL NAVIGATION (SIDEBAR + BACKUP) ---
# If the sidebar is hidden, the user can still use session state to navigate
if "page" not in st.session_state:
    st.session_state.page = "🔍 Research"

with st.sidebar:
    st.markdown("<h2 style='color:#8ab4f8'>♊ Vantage AI</h2>", unsafe_allow_html=True)
    # This is your Hamburger Menu logic
    nav_choice = st.radio("Menu", ["🔍 Research", "📈 Crypto Market", "💻 Code Architect"], label_visibility="collapsed")
    st.session_state.page = nav_choice
    st.divider()
    st.subheader("📁 Analysis")
    uploaded_file = st.file_uploader("Upload Chart", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

# --- 4. PAGE LOGIC ---

# PAGE: RESEARCH
if st.session_state.page == "🔍 Research":
    st.title("Intelligence Hub")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask Vantage..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            content = [prompt, Image.open(uploaded_file)] if uploaded_file else prompt
            response = model.generate_content(content)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

# PAGE: CRYPTO MARKET (THE MISSING TABS)
elif st.session_state.page == "📈 Crypto Market":
    st.title("Global Terminal")
    
    # These are the sub-sections under the Crypto Tab
    tab_majors, tab_memes, tab_metals, tab_trends = st.tabs([
        "💎 Major Crypto", "🚀 Meme Coins", "🛡️ Gold & Silver", "🔮 Moonshot Scanner"
    ])
    
    with tab_majors:
        st.subheader("Live Market: Bitcoin & Ethereum")
        components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=60&theme=dark" width="100%" height="500"></iframe>', height=500)
    
    with tab_memes:
        st.subheader("Meme Coin Tracker")
        ticker = st.selectbox("Select Coin", ["PEPEUSDT", "DOGEUSDT", "SHIBUSDT", "BONKUSDT"])
        components.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:{ticker}&interval=5&theme=dark" width="100%" height="450"></iframe>', height=450)
        
    with tab_metals:
        c1, c2 = st.columns(2)
        with c1:
            st.caption("GOLD SPOT")
            components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=TVC:GOLD&theme=dark" width="100%" height="300"></iframe>', height=300)
        with c2:
            st.caption("SILVER SPOT")
            components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=TVC:SILVER&theme=dark" width="100%" height="300"></iframe>', height=300)

    with tab_trends:
        st.subheader("AI Market Analysis")
        if st.button("Scan for Upcoming Trends"):
            with st.spinner("Analyzing Solana & Base volume..."):
                scan = model.generate_content("Analyze current trending meme coins and identify 3 with high potential based on 2026 market signals.")
                st.write(scan.text)

# PAGE: CODING
elif st.session_state.page == "💻 Code Architect":
    st.title("Code Architect")
    task = st.text_area("Describe the project...")
    if st.button("Build Code"):
        res = model.generate_content(f"Write clean code for: {task}")
        st.code(res.text)