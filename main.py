import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
from PIL import Image

# --- 1. GEMINI ELITE CONFIG ---
st.set_page_config(page_title="Vantage AI", page_icon="♊", layout="wide", initial_sidebar_state="expanded")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. THE "ANTI-CHEAP" CSS (Gemini UI Clone) ---
st.markdown("""
    <style>
    /* Google Gemini Dark Theme Palette */
    :root {
        --bg-dark: #131314;
        --sidebar-bg: #1e1f20;
        --text-main: #e3e3e3;
        --accent-blue: #8ab4f8;
        --glass: rgba(255, 255, 255, 0.05);
    }

    .main { background-color: var(--bg-dark); color: var(--text-main); font-family: 'Google Sans', Arial, sans-serif; }
    
    /* Hide the 'cheap' Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sleek Sidebar Navigation */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg);
        border-right: 1px solid #3c4043;
        width: 280px !important;
    }

    /* Floating Gemini Chat Bubbles */
    .stChatMessage {
        background-color: var(--glass) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    /* Professional Input Bar */
    .stChatInputContainer {
        padding: 20px !important;
        background-color: transparent !important;
    }
    .stChatInput {
        border-radius: 30px !important;
        border: 1px solid #5f6368 !important;
        background-color: #1e1f20 !important;
    }

    /* Modern Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 20px;
        border: 1px solid #3c4043;
        padding: 8px 20px;
        color: #9aa0a6;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3c4043 !important;
        color: white !important;
        border: 1px solid var(--accent-blue) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (The Hamburger Menu) ---
with st.sidebar:
    st.title("Vantage AI")
    st.caption("2026 Enterprise Edition")
    st.divider()
    # Using a cleaner navigation style
    page = st.selectbox("Navigation", ["Research Lab", "Code Architect", "Asset Terminal"])
    st.divider()
    
    st.subheader("📁 Image Intelligence")
    uploaded_file = st.file_uploader("Upload for AI Vision", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)

# --- 4. NAVIGATION LOGIC ---

if page == "Research Lab":
    st.markdown("<h2 style='text-align: center;'>How can I help you today?</h2>", unsafe_allow_html=True)
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask Vantage..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            # Real-time 'Thinking' animation
            with st.spinner(" "):
                content = [prompt, Image.open(uploaded_file)] if uploaded_file else prompt
                response = model.generate_content(content)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

elif page == "Asset Terminal":
    st.title("Market Terminal")
    t1, t2, t3 = st.tabs(["Majors", "Meme Coins", "Precious Metals"])
    
    with t1:
        # Pinned live feed at top
        components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=15&theme=dark" width="100%" height="500"></iframe>', height=500)
    
    with t2:
        meme = st.selectbox("Select Meme Token", ["PEPEUSDT", "DOGEUSDT", "SHIBUSDT"])
        components.html(f'<iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:{meme}&interval=5&theme=dark" width="100%" height="400"></iframe>', height=400)

    with t3:
        col1, col2 = st.columns(2)
        with col1: components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=TVC:GOLD&theme=dark" width="100%" height="300"></iframe>', height=300)
        with col2: components.html('<iframe src="https://s.tradingview.com/widgetembed/?symbol=TVC:SILVER&theme=dark" width="100%" height="300"></iframe>', height=300)

elif page == "Code Architect":
    st.title("Code Architect")
    task = st.text_area("Describe the software logic...")
    if st.button("Generate Script"):
        res = model.generate_content(f"Write high-end code for: {task}")
        st.code(res.text)