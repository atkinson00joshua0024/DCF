import streamlit as st
 
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
    .metric-sub.red { color: #ef5350; }
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
    .download-btn {
        display: block;
        background: #2563eb;
        color: white !important;
        text-align: center;
        padding: 16px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        text-decoration: none;
        margin-top: 24px;
    }
    .tag-bull { background: #1a3a2a; color: #4caf50; padding: 3px 10px; border-radius: 20px; font-size: 12px; }
    .tag-bear { background: #3a1a1a; color: #ef5350; padding: 3px 10px; border-radius: 20px; font-size: 12px; }
    .tag-base { background: #1a2a3a; color: #64b5f6; padding: 3px 10px; border-radius: 20px; font-size: 12px; }
</style>
""", unsafe_allow_html=True)
 
st.markdown("## 🏰 Walt Disney Company — DCF Valuation")
st.markdown("*Financial modeling exercise for educational purposes only. Not investment advice.*")
 
# --- Top metrics ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""<div class="metric-card">
        <div class="metric-label">Estimated Share Price</div>
        <div class="metric-value">$157.31</div>
        <div class="metric-sub">Base Case</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="metric-card">
        <div class="metric-label">Current Stock Price</div>
        <div class="metric-value">$119.54</div>
        <div class="metric-sub" style="color:#8b92a5">As of model date</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="metric-card">
        <div class="metric-label">Upside / Downside</div>
        <div class="metric-value" style="color:#4caf50">+31.6%</div>
        <div class="metric-sub">Undervalued</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""<div class="metric-card">
        <div class="metric-label">Equity Value</div>
        <div class="metric-value">$283B</div>
        <div class="metric-sub" style="color:#8b92a5">1,800M shares</div>
    </div>""", unsafe_allow_html=True)
 
# --- Two columns: Valuation bridge + WACC ---
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
for col, case, price, upside, tag_class in [
    (col_s1, "Bear Case", "$98.40", "-17.7%", "tag-bear"),
    (col_s2, "Base Case", "$157.31", "+31.6%", "tag-base"),
    (col_s3, "Bull Case", "$209.45", "+75.2%", "tag-bull"),
]:
    with col:
        color = "#ef5350" if "-" in upside else "#4caf50" if "+" in upside else "#64b5f6"
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">{case}</div>
            <div class="metric-value">{price}</div>
            <div class="metric-sub" style="color:{color}">{upside} vs current</div>
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
