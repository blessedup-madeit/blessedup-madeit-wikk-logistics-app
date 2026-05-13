import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
from PIL import Image

# --- 1. CORE CONFIG ---
st.set_page_config(
    page_title="Vantage Elite AI", 
    page_icon="♊", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. UPDATED MODEL (MAY 2026 STABLE) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # gemini-3.1-flash-lite is the new May 2026 stable workhorse
    model = genai.GenerativeModel('gemini-3.1-flash-lite') 
else:
    st.error("API Key missing in Streamlit Secrets!")

# --- 3. PREMIUM DARK UI ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e10; color: #e3e3e3; }
    [data-testid="stSidebar"] { background-color: #1e1f20 !important; border-right: 1px solid #333; }
    .stChatMessage { background-color: #1c1c1e !important; border-radius: 15px !important; border: 1px solid #2c2c2e !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION ---
if "page" not in st.session_state:
    st.session_state.page = "🔍 Research"

with st.sidebar:
    st.markdown("<h2 style='color:#8ab4f8'>♊ Vantage AI</h2>", unsafe_allow_html=True)
    nav = st.radio("Navigation", ["🔍 Research", "📈 Market Terminal", "💻 Code Architect"], label_visibility="collapsed")
    st.session_state.page = nav
    st.divider()
    uploaded_file = st.file_uploader("Upload Visual Data", type=['png', 'jpg', 'jpeg'])

# --- 5. PAGE: RESEARCH (FIXED ERROR) ---
if st.session_state.page == "🔍 Research":
    st.title("Intelligence Hub")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Ask Vantage..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                # Combining vision and text logic for the new 3.1 model
                content = [prompt, Image.open(uploaded_file)] if uploaded_file else [prompt]
                response = model.generate_content(content)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"⚠️ API Connection Error: {e}")

# --- 6. PAGE: MARKET TERMINAL (GLOBAL SCREENER) ---
elif st.session_state.page == "📈 Market Terminal":
    st.title("Global Market Intel")
    
    tab_global, tab_scanner = st.tabs(["🌎 All Crypto & Memes", "🔮 AI Moonshot Scanner"])
    
    with tab_global:
        st.subheader("Interactive Crypto Screener")
        st.caption("Filter by Performance, Popularity, and Growth using the 'Filters' button inside the widget below.")
        
        # This is a full-featured screener. You can filter for ALL coins/memes here.
        components.html("""
            <div class="tradingview-widget-container">
              <iframe src="https://www.tradingview-widgets.com/embed-widget/crypto-mkt-screener/?customer=binance&theme=dark" width="100%" height="600" frameborder="0"></iframe>
            </div>
        """, height=620)
    
    with tab_scanner:
        st.subheader("AI Trend Analysis")
        if "scan_data" not in st.session_state: st.session_state.scan_data = None
        
        if st.button("Run Deep Scan"):
            with st.spinner("Processing social and volume data..."):
                try:
                    res = model.generate_content("Analyze current high-growth meme coins for 2026. Highlight risk vs reward.")
                    st.session_state.scan_data = res.text
                except Exception as e:
                    st.error(f"Scanner Error: {e}")
        
        if st.session_state.scan_data:
            st.markdown(st.session_state.scan_data)

# --- 7. PAGE: CODING ---
elif st.session_state.page == "💻 Code Architect":
    st.title("Code Architect")
    task = st.text_area("Describe the project...")
    if st.button("Generate Script"):
        try:
            res = model.generate_content(f"Write high-quality code for: {task}")
            st.code(res.text)
        except Exception as e:
            st.error(f"Coding AI Error: {e}")