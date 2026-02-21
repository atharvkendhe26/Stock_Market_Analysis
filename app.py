import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Global Financial Trading Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Global Financial Trading Dashboard")
st.markdown("Interactive stock market analysis by Country and Company")

# ---------------- LOAD DATA ---------------- #
@st.cache_data
def load_data():
    df = pd.read_csv("Global_Financial_Data.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

df = load_data()

# ---------------- SIDEBAR ---------------- #
st.sidebar.header("🔎 Filter Stocks")

# Country selection
countries = df["Country"].dropna().unique()
selected_country = st.sidebar.selectbox("🌍 Select Country", sorted(countries))

# Filter country
country_df = df[df["Country"] == selected_country]

# Company selection
companies = country_df["Company"].dropna().unique()
selected_company = st.sidebar.selectbox("🏢 Select Company", sorted(companies))

# Filter company
company_df = country_df[country_df["Company"] == selected_company]

# Date Range
min_date = company_df["Date"].min()
max_date = company_df["Date"].max()

start_date, end_date = st.sidebar.date_input(
    "📅 Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

filtered_df = company_df[
    (company_df["Date"] >= pd.to_datetime(start_date)) &
    (company_df["Date"] <= pd.to_datetime(end_date))
]

# ---------------- MAIN LAYOUT ---------------- #
col1, col2 = st.columns([3, 1])

# ===================== CHART AREA ===================== #
with col1:
    st.subheader(f"📈 Stock Chart - {selected_company}")

    chart_type = st.radio(
        "Select Chart Type",
        ["Line Chart", "Candlestick Chart"],
        horizontal=True
    )

    if chart_type == "Line Chart":
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["Open"],
            mode="lines",
            name="Open",
            line=dict(color="blue")
        ))

        fig.add_trace(go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["Close"],
            mode="lines",
            name="Close",
            line=dict(color="green")
        ))

        fig.add_trace(go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["High"],
            mode="lines",
            name="High",
            line=dict(color="orange")
        ))

        fig.add_trace(go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df["Low"],
            mode="lines",
            name="Low",
            line=dict(color="red")
        ))

        fig.update_layout(
            template="plotly_dark",
            height=600,
            xaxis_title="Date",
            yaxis_title="Stock Price",
            legend_title="Indicators"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        fig = go.Figure(data=[go.Candlestick(
            x=filtered_df["Date"],
            open=filtered_df["Open"],
            high=filtered_df["High"],
            low=filtered_df["Low"],
            close=filtered_df["Close"],
            increasing_line_color="green",
            decreasing_line_color="red"
        )])

        fig.update_layout(
            template="plotly_dark",
            height=600,
            xaxis_title="Date",
            yaxis_title="Price"
        )

        st.plotly_chart(fig, use_container_width=True)


# ===================== DETAILS PANEL ===================== #
with col2:
    st.subheader("📌 Stock Details")

    if not filtered_df.empty:
        latest = filtered_df.iloc[-1]

        st.metric("💰 Latest Close", f"{latest['Close']:.2f}")
        st.metric("📊 Open", f"{latest['Open']:.2f}")
        st.metric("📈 High", f"{latest['High']:.2f}")
        st.metric("📉 Low", f"{latest['Low']:.2f}")
        st.metric("🔄 Volume", f"{latest['Volume']:,.0f}")

        st.markdown("---")
        st.write("📅 Date:", latest["Date"].date())
        st.write("🌍 Country:", selected_country)
        st.write("🏢 Company:", selected_company)

# ---------------- DATA TABLE ---------------- #
st.markdown("---")
st.subheader("📋 Stock Data Table")
st.dataframe(filtered_df, use_container_width=True)

# ---------------- DOWNLOAD BUTTON ---------------- #
st.download_button(
    "⬇ Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="filtered_stock_data.csv",
    mime="text/csv"
)

st.markdown("✨ Designed like a Trading Platform using Streamlit")
