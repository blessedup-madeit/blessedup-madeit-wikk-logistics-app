import streamlit as st
import google.generativeai as genai
from PIL import Image
import streamlit.components.v1 as components

# --- 1. CORE SETTINGS ---
st.set_page_config(page_title="Vantage Elite", page_icon="♊", layout="wide")

# Connect to your API key in secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. THE "ULTRA-DARK" UI OVERHAUL ---
st.markdown("""
    <style>
    /* Gemini 2026 Dark Palette */
    .stApp {
        background-color: #0e0e10;
        color: #e3e3e3;
    }
    
    /* Custom Top Navigation Bar */
    .nav-bar {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 50px;
        margin-bottom: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Professional Chat Bubbles */
    [data-testid="stChatMessage"] {
        background-color: #1e1f20 !important;
        border: 1px solid #333 !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Glowing Inputs */
    .stChatInputContainer input {
        border: 1px solid #444 !important;
        background-color: #1e1f20 !important;
        border-radius: 30px !important;
    }
    
    /* TradingView Widget Container */
    .tradingview-widget-container {
        border-radius: 15px;
        overflow: hidden;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CUSTOM NAVIGATION LOGIC ---
# Using a cleaner state-based navigation instead of the sidebar dropdown
if "current_page" not in st.session_state:
    st.session_state.current_page = "Research Lab"

# Horizontal Navigation Menu
cols = st.columns([1,1,1,1,1])
with cols[1]:
    if st.button("🔍 Research Lab", use_container_width=True): st.session_state.current_page = "Research Lab"
with cols[2]:
    if st.button("📈 Asset Terminal", use_container_width=True): st.session_state.current_page = "Asset Terminal"
with cols[3]:
    if st.button("💻 Code Architect", use_container_width=True): st.session_state.current_page = "Code Architect"

st.divider()

# --- 4. PAGE: RESEARCH LAB (The AI Hub) ---
if st.session_state.current_page == "Research Lab":
    st.markdown("<h1 style='text-align: center; color: #8ab4f8;'>Vantage Intelligence</h1>", unsafe_allow_html=True)
    
    # Image upload moved to a cleaner spot
    with st.expander("📸 Attach Visual Data (Charts, Docs, Images)"):
        uploaded_file = st.file_uploader("Upload", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        if uploaded_file: st.image(uploaded_file, width=300)

    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                content = [prompt, Image.open(uploaded_file)] if uploaded_file else prompt
                response = model.generate_content(content)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- 5. PAGE: ASSET TERMINAL (Live Markets) ---
elif st.session_state.current_page == "Asset Terminal":
    st.title("Market Terminal")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Live Chart Analysis")
        symbol = st.selectbox("Select Asset", ["BTCUSDT", "ETHUSDT", "GOLD", "TSLA", "SOLUSDT"])
        # Professional 2026 TradingView Widget
        components.html(f"""
            <div class="tradingview-widget-container">
                <iframe src="https://s.tradingview.com/widgetembed/?symbol={symbol}&interval=1D&theme=dark" width="100%" height="500"></iframe>
            </div>
        """, height=520)
        
    with col2:
        st.subheader("Market Heatmap")
        components.html("""
            <iframe src="https://www.tradingview-widgets.com/embed-widget/crypto-mkt-screener/?theme=dark" width="100%" height="500"></iframe>
        """, height=520)

# --- 6. PAGE: CODE ARCHITECT ---
elif st.session_state.current_page == "Code Architect":
    st.title("Code Architect")
    st.info("Describe your project and I'll build the Python/CSS structure.")
    
    c1, c2 = st.columns(2)
    with c1:
        code_input = st.text_area("Describe the logic you need...", height=300)
    
    if st.button("🔨 Build System"):
        with st.spinner("Architecting..."):
            res = model.generate_content(f"Provide clean, professional code for: {code_input}")
            with c2:
                st.code(res.text, language='python')