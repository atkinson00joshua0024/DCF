import streamlit as st
import urllib.request
import json

st.set_page_config(layout="wide", page_title="Disney DCF Valuation")

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: #1e2130;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        border: 1px solid #2e3250;
    }
    .metric-label { color: #8b92a5; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .metric-value { color: #ffffff; font-size: 32px; font-weight: 700; }
    .metric-sub { color: #4caf50; font-size: 14px; margin-top: 6px; }
    .section-title { color: #8b92a5; font-size: 12px; text-transform: uppercase; letter-spacing: 2px; margin: 32px 0 12px 0; }
    .row-card {
        background: #1e2130;
        border-radius: 10px;
        padding: 16px 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #2e3250;
        margin-bottom: 8px;
    }
    .row-label { color: #8b92a5; font-size: 14px; }
    .row-value { color: #ffffff; font-size: 15px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🏰 Walt Disney Company — DCF Valuation")
st.markdown("*Financial modeling exercise for educational purposes only. Not investment advice.*")

# --- Fetch live DIS price ---
@st.cache_data(ttl=3600)  # refresh every hour
def get_dis_price():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/DIS?interval=1d&range=1d"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
        price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        return round(price, 2)
    except:
        return 119.54  # fallback to model date price

current_price = get_dis_price()
estimated_price = 157.31
upside = (estimated_price - current_price) / current_price
upside_color = "#4caf50" if upside > 0 else "#ef5350"
upside_label = "Undervalued" if upside > 0 else "Overvalued"

# --- Top metrics ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Estimated Share Price</div>
        <div class="metric-value">$157.31</div>
        <div class="metric-sub">Base Case</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Current Stock Price</div>
        <div class="metric-value">${current_price:.2f}</div>
        <div class="metric-sub" style="color:#8b92a5">Live — updates hourly</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Upside / Downside</div>
        <div class="metric-value" style="color:{upside_color}">{upside:+.1%}</div>
        <div class="metric-sub" style="color:{upside_color}">{upside_label}</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-label">Equity Value</div>
        <div class="metric-value">$283B</div>
        <div class="metric-sub" style="color:#8b92a5">1,800M shares</div>
    </div>""", unsafe_allow_html=True)

# --- Valuation bridge + WACC ---
st.markdown('<div class="section-title">Valuation Bridge</div>', unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a:
    for label, value in [
        ("Sum of Projected FCFF", "$59,083M"),
        ("PV of Terminal Value", "$190,954M"),
        ("Total Enterprise Value", "$250,037M"),
        ("Less: Net Debt", "$33,128M"),
        ("Equity Value", "$283,165M"),
    ]:
        st.markdown(f"""<div class="row-card">
            <span class="row-label">{label}</span>
            <span class="row-value">{value}</span>
        </div>""", unsafe_allow_html=True)

with col_b:
    for label, value in [
        ("WACC", "9.29%"),
        ("Terminal Growth Rate", "3.00%"),
        ("Risk-Free Rate", "4.44%"),
        ("Beta", "1.56"),
        ("Cost of Equity", "10.77%"),
        ("Tax Rate", "23.73%"),
    ]:
        st.markdown(f"""<div class="row-card">
            <span class="row-label">{label}</span>
            <span class="row-value">{value}</span>
        </div>""", unsafe_allow_html=True)

# --- Scenarios ---
st.markdown('<div class="section-title">Scenario Analysis</div>', unsafe_allow_html=True)
col_s1, col_s2, col_s3 = st.columns(3)
for col, case, price_val in [
    (col_s1, "Bear Case", 98.40),
    (col_s2, "Base Case", 157.31),
    (col_s3, "Bull Case", 209.45),
]:
    with col:
        diff = (price_val - current_price) / current_price
        color = "#4caf50" if diff > 0 else "#ef5350"
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">{case}</div>
            <div class="metric-value">${price_val:.2f}</div>
            <div class="metric-sub" style="color:{color}">{diff:+.1%} vs current</div>
        </div>""", unsafe_allow_html=True)

# --- Download ---
st.markdown('<div class="section-title">Full Model</div>', unsafe_allow_html=True)
with open("Disney_DCF_Valuation.xlsx", "rb") as f:
    st.download_button(
        label="📥 Download Full Excel Model",
        data=f,
        file_name="Disney_DCF_Valuation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
