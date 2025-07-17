import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests

# ------------------------------------------------------------
# Page config
# ------------------------------------------------------------
st.set_page_config(page_title="US Car Export Analyzer", page_icon="🚗", layout="wide")

# ------------------------------------------------------------
# Live USD→EUR FX rate (exchangerate.host)
# Cached 1h to avoid rate limits
# ------------------------------------------------------------
@st.cache_data(ttl=3600)
def get_live_usd_to_eur() -> float:
    url = "https://api.exchangerate.host/latest?base=USD&symbols=EUR"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        return float(data["rates"]["EUR"])
    except Exception:
        # fallback default if API fails
        return 0.92

# ------------------------------------------------------------
# Data loader (placeholder simulated data)
# Replace with real API / scraping results
# ------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data(model_name: str, min_year: int, max_year: int, n: int = 200) -> pd.DataFrame:
    np.random.seed(42)
    data = {
        "Model": [model_name] * n,
        "Year": np.random.randint(min_year, max_year + 1, n),
        "Price_USD": np.random.randint(25_000, 90_000, n),
        "Mileage_miles": np.random.randint(5_000, 120_000, n),
        "State": np.random.choice(
            ["CA", "TX", "FL", "NY", "NJ", "IL", "WA", "GA", "AZ", "CO"], n
        ),
    }
    return pd.DataFrame(data)

# ------------------------------------------------------------
# Sidebar filters
# ------------------------------------------------------------
st.sidebar.header("Filter Options")
model = st.sidebar.text_input("Car Model (e.g., BMW M3 E92)", "BMW M3 E92")
min_year = st.sidebar.number_input("Min Year", min_value=1990, max_value=2025, value=2008)
max_year = st.sidebar.number_input("Max Year", min_value=1990, max_value=2025, value=2013)
n_rows = st.sidebar.slider("# Listings (simulated)", min_value=50, max_value=1000, value=200, step=50)

with st.spinner("Loading data & FX rate..."):
    df = load_data(model, min_year, max_year, n_rows)
    fx_rate = get_live_usd_to_eur()

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.title("US Car Market Analysis for Export")
st.caption("Demo with simulated data + live USD→EUR exchange rate (exchangerate.host).")

# FX display + manual override
col_fx1, col_fx2 = st.columns([1,1])
with col_fx1:
    st.info(f"Current USD→EUR rate (live): {fx_rate:.4f}")
with col_fx2:
    manual_fx = st.number_input("Override FX? Leave =0 to use live rate", value=0.0, step=0.0001, format="%.4f")
active_fx = manual_fx if manual_fx > 0 else fx_rate

# ------------------------------------------------------------
# Data preview
# ------------------------------------------------------------
st.subheader("Sample Listings")
st.dataframe(df.head(20), use_container_width=True)

# ------------------------------------------------------------
# Market snapshot
# ------------------------------------------------------------
st.subheader("Market Snapshot")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Average Price (USD)", f"${df['Price_USD'].mean():,.0f}")
with col2:
    st.metric("Median Price (USD)", f"${df['Price_USD'].median():,.0f}")
with col3:
    st.metric("Lowest Price (USD)", f"${df['Price_USD'].min():,.0f}")
with col4:
    st.metric("Highest Price (USD)", f"${df['Price_USD'].max():,.0f}")

# ------------------------------------------------------------
# Visualizations
# ------------------------------------------------------------
colA, colB = st.columns(2)
with colA:
    fig_hist = px.histogram(df, x="Price_USD", nbins=25, title="Price Distribution (USD)")
    st.plotly_chart(fig_hist, use_container_width=True)
with colB:
    fig_scatter = px.scatter(
        df, x="Mileage_miles", y="Price_USD", color="Year", title="Price vs Mileage", hover_data=["State"]
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ------------------------------------------------------------
# Import Cost & Profit Calculator
# ------------------------------------------------------------
st.header("Import Cost & Profit Simulation")

default_purchase = int(df["Price_USD"].mean()) if not df.empty else 40_000
purchase_price_usd = st.number_input("Purchase Price (USD)", value=default_purchase, step=1000)
purchase_price_eur = purchase_price_usd * active_fx

st.markdown("### Import Cost Assumptions")
colc1, colc2, colc3 = st.columns(3)
with colc1:
    shipping = st.number_input("Shipping (€)", value=2000, step=100)
with colc2:
    duty_pct = st.number_input("Duties (% of value)", value=10.0, step=0.5)
with colc3:
    vat_pct = st.number_input("VAT (%)", value=22.0, step=0.5)

colc4, colc5 = st.columns(2)
with colc4:
    omolog = st.number_input("Omologazione & Mods (€)", value=2500, step=100)
with colc5:
    other_fees = st.number_input("Other Fees (€)", value=1000, step=100)

duty = (duty_pct / 100.0) * purchase_price_eur
vat = (vat_pct / 100.0) * (purchase_price_eur + duty + shipping)
landed_cost = purchase_price_eur + shipping + duty + vat + omolog + other_fees

st.markdown("### EU Sale Price Scenario")
sale_price = st.number_input("Expected Sale Price in EU (€)", value=60000, step=1000)
profit = sale_price - landed_cost

st.markdown(f"**Estimated Landed Cost:** €{landed_cost:,.0f}")
st.markdown(f"**Projected Profit:** €{profit:,.0f}")

if profit > 0:
    st.success("✅ Potentially profitable")
else:
    st.error("❌ Likely unprofitable")

# ------------------------------------------------------------
# Data export
# ------------------------------------------------------------
st.download_button(
    "Download current dataset (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="us_car_market_sample.csv",
    mime="text/csv",
)
