import streamlit as st
import google.generativeai as genai
import requests
import streamlit.components.v1 as components
from PIL import Image

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="Vantage Trading Pro", page_icon="📈", layout="wide")

# Configure AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- DARK TERMINAL STYLING ---
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stMetric { background-color: #111; border: 1px solid #333; padding: 15px; border-radius: 10px; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: TRADING CONTROLS ---
with st.sidebar:
    st.title("⚡ Vantage Terminal")
    st.subheader("Asset Selection")
    asset_symbol = st.text_input("Enter Ticker (e.g. BTCUSD, PEPEUSDT)", "BTCUSD").upper()
    
    st.divider()
    st.subheader("Day Trading Tools")
    st.info("AI Analysis: Technical / Sentiment / Volatility")
    if st.button("Analyze Current Trend"):
        with st.spinner("Scanning Market..."):
            # Deep scan prompt for Day Trading
            analysis_prompt = f"Act as a professional day trader. Analyze {asset_symbol}. Discuss support/resistance levels, current volume trends for meme coins or majors, and potential 24-hour outlook."
            response = model.generate_content(analysis_prompt)
            st.write(response.text)

# --- MAIN INTERFACE: THE TERMINAL ---
col_chart, col_chat = st.columns([2, 1])

with col_chart:
    st.subheader(f"🔴 Live Market Feed: {asset_symbol}")
    
    # TRADINGVIEW LIVE CHART WIDGET
    tradingview_html = f"""
    <div class="tradingview-widget-container" style="height: 500px;">
      <div id="tradingview_chart"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true,
        "symbol": "{asset_symbol}",
        "interval": "15",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_chart"
      }});
      </script>
    </div>
    """
    components.html(tradingview_html, height=500)
    
    # Real-time Metrics (Finnhub fallback for stats)
    m_col1, m_col2, m_col3 = st.columns(3)
    try:
        r = requests.get(f"https://finnhub.io/api/v1/quote?symbol={asset_symbol.replace('USD', '')}&token={st.secrets['FINNHUB_API_KEY']}").json()
        if 'c' in r:
            m_col1.metric("Current Price", f"${r['c']:,}")
            m_col2.metric("24h High", f"${r['h']:,}")
            m_col3.metric("Daily Change", f"{r['dp']}%")
    except:
        st.caption("Detailed metrics loading...")

with col_chat:
    st.subheader("🧠 Vantage Intelligence")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about meme coins, trends, or trade setups..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            # Fetch context to make AI smarter
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(f"Using current {asset_symbol} data, answer this: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})