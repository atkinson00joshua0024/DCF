import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Disney DCF Valuation")
st.title("🏰 Walt Disney Company — DCF Valuation Model")

# --- Load Excel ---
@st.cache_data
def load_data():
    xl = pd.ExcelFile("Disney_DCF_Valuation.xlsx")
    return xl

xl = load_data()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 DCF Summary",
    "🔢 Sensitivity Analysis",
    "📈 Forecasted Assumptions",
    "📋 Financials",
    "ℹ️ About"
])

# ─────────────────────────────────────────────
# TAB 1: DCF SUMMARY
# ─────────────────────────────────────────────
with tab1:
    st.header("DCF Valuation Summary")

    # Hardcoded from model output
    dcf = {
        "WACC": 0.09293,
        "Terminal Growth Rate": 0.03,
        "Sum of Projected FCFF ($M)": 59083.49,
        "Terminal Value ($M)": 297777.75,
        "PV Terminal Value ($M)": 190953.62,
        "Total Enterprise Value ($M)": 250037.11,
        "Net Debt ($M)": 33128.0,
        "Equity Value ($M)": 283165.11,
        "Shares Outstanding (M)": 1800,
        "Estimated Share Price": 157.31,
        "Current Stock Price": 119.54,
        "Upside / Downside": 0.316,
        "Active Case": "Base",
    }

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Estimated Share Price", f"${dcf['Estimated Share Price']:.2f}")
    col2.metric("Current Stock Price", f"${dcf['Current Stock Price']:.2f}")
    col3.metric("Upside / Downside", f"{dcf['Upside / Downside']:.1%}")
    col4.metric("Active Case", dcf["Active Case"])

    st.markdown("---")
    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Valuation Bridge ($M)")
        bridge_data = {
            "Component": [
                "Sum of Projected FCFF",
                "PV of Terminal Value",
                "Total Enterprise Value",
                "Less: Net Debt",
                "Equity Value"
            ],
            "Value ($M)": [
                dcf["Sum of Projected FCFF ($M)"],
                dcf["PV Terminal Value ($M)"],
                dcf["Total Enterprise Value ($M)"],
                dcf["Net Debt ($M)"],
                dcf["Equity Value ($M)"]
            ]
        }
        bridge_df = pd.DataFrame(bridge_data)
        bridge_df["Value ($M)"] = bridge_df["Value ($M)"].apply(lambda x: f"${x:,.0f}M")
        st.dataframe(bridge_df, use_container_width=True, hide_index=True)

    with col6:
        st.subheader("WACC Components")
        wacc_data = {
            "Component": [
                "Risk-Free Rate", "Beta", "Market Return",
                "Cost of Equity", "Pre-Tax Cost of Debt",
                "After-Tax Cost of Debt", "Equity Weight", "Debt Weight", "WACC"
            ],
            "Value": [
                "4.44%", "1.56", "8.50%",
                "10.77%", "1.52%",
                "1.16%", "84.60%", "15.40%", "9.29%"
            ]
        }
        st.dataframe(pd.DataFrame(wacc_data), use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("Free Cash Flow Build ($M)")
    fcff_data = {
        "Metric": ["EBIT", "Taxes", "NOPAT", "D&A", "NCWC", "Capex", "FCFF", "FCFF Growth"],
        "2025E": [11564.2, -2744.2, 8820.0, 5139.7, -254.6, -5574.4, 8130.8, "N/A"],
        "2026E": [13984.1, -3318.4, 10665.6, 5345.3, -349.6, -5797.3, 9864.0, "21.3%"],
        "2027E": [15814.8, -3752.9, 12062.0, 5559.1, -363.6, -6029.2, 11228.3, "13.8%"],
        "2028E": [16368.3, -3884.2, 12484.1, 5753.7, -330.8, -6240.3, 11666.7, "3.9%"],
        "2029E": [18937.1, 0.0, 18937.1, 5897.5, -244.6, -6396.3, 18193.7, "55.9%"],
    }
    st.dataframe(pd.DataFrame(fcff_data), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# TAB 2: SENSITIVITY ANALYSIS
# ─────────────────────────────────────────────
with tab2:
    st.header("Sensitivity Analysis — Estimated Share Price")
    st.write("Share price at varying WACC and Terminal Growth Rate combinations.")

    wacc_rates = [0.0729, 0.0779, 0.0829, 0.0879, 0.0929, 0.0979, 0.1029, 0.1079, 0.1129]
    tgr_rates = [0.02, 0.025, 0.03, 0.035, 0.04]

    sensitivity = {
        0.0729: [188.32, 203.37, 221.93, 245.39, 275.97],
        0.0779: [173.60, 185.82, 200.60, 218.82, 241.84],
        0.0829: [161.30, 171.39, 183.39, 197.89, 215.77],
        0.0879: [150.87, 159.32, 169.22, 181.00, 195.24],
        0.0929: [141.93, 149.09, 157.38, 167.11, 178.67],
        0.0979: [134.19, 140.32, 147.35, 155.49, 165.04],
        0.1029: [127.44, 132.73, 138.74, 145.64, 153.64],
        0.1079: [121.50, 126.10, 131.29, 137.20, 143.98],
        0.1129: [116.23, 120.27, 124.79, 129.89, 135.69],
    }

    sens_df = pd.DataFrame(
        sensitivity,
        index=[f"{r:.1%}" for r in tgr_rates]
    ).T
    sens_df.index = [f"{r:.2%}" for r in wacc_rates]
    sens_df.index.name = "WACC \\ TGR"
    sens_df.columns.name = None

    # Highlight the base case cell
    def highlight_base(val):
        try:
            v = float(val)
            if 156 < v < 159:
                return "background-color: #ffe066; font-weight: bold"
            elif v > dcf["Current Stock Price"]:
                return "color: green"
            else:
                return "color: red"
        except:
            return ""

    styled = sens_df.style.format("${:.2f}").applymap(highlight_base)
    st.dataframe(styled, use_container_width=True)

    st.caption("🟡 Yellow = Base case (~$157). Green = above current price ($119.54). Red = below current price.")

    st.markdown("---")
    st.subheader("Implied Upside at Each Scenario")
    upside_df = (sens_df - dcf["Current Stock Price"]) / dcf["Current Stock Price"]
    styled_upside = upside_df.style.format("{:.1%}").background_gradient(cmap="RdYlGn", vmin=-0.2, vmax=0.5)
    st.dataframe(styled_upside, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 3: FORECASTED ASSUMPTIONS
# ─────────────────────────────────────────────
with tab3:
    st.header("Forecasted Assumptions")
    try:
        raw = pd.read_excel("Disney_DCF_Valuation.xlsx", sheet_name="Forecasted Assumptions", header=None)
        st.dataframe(raw, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load sheet: {e}")

# ─────────────────────────────────────────────
# TAB 4: FINANCIALS
# ─────────────────────────────────────────────
with tab4:
    st.header("Historical Financials")

    sheet_names = xl.sheet_names
    financial_sheets = [s for s in sheet_names if s not in ["DCF Valuation", "Forecasted Assumptions"]]

    if financial_sheets:
        selected_sheet = st.selectbox("Select Statement", financial_sheets)
        try:
            df = pd.read_excel("Disney_DCF_Valuation.xlsx", sheet_name=selected_sheet, header=None)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Could not load sheet: {e}")
    else:
        st.info("No additional financial statement sheets found.")

# ─────────────────────────────────────────────
# TAB 5: ABOUT
# ─────────────────────────────────────────────
with tab5:
    st.header("About This Model")
    st.markdown("""
    This dashboard presents a **Discounted Cash Flow (DCF) valuation** of The Walt Disney Company.

    **Methodology:**
    - **FCFF** (Free Cash Flow to the Firm) is projected over a 5-year period (2025E–2029E)
    - A **terminal value** is calculated using the Gordon Growth Model at a 3% perpetuity growth rate
    - Cash flows and terminal value are discounted at the **WACC** to arrive at Enterprise Value
    - Net debt is subtracted to derive **Equity Value**, then divided by shares outstanding for a per-share price

    **Key Assumptions (Base Case):**
    - WACC: 9.29%
    - Terminal Growth Rate: 3.0%
    - Tax Rate: 23.73%
    - Shares Outstanding: 1,800M

    **Three Scenarios modeled:** Base, Bear, Bull — toggle via the Case Toggle in the original Excel model.

    **Disclaimer:** This is a financial modeling exercise for educational purposes only. Not investment advice.
    """)
