import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Price Comparison", layout="wide")
st.title("📊 Price Comparison Across Websites")

# Check if scraped data exists
if "scraped_data" not in st.session_state:
    st.warning("No data found. Please scrape products first.")
    st.page_link("main.py", label="🔍 Go Scrape Data First", icon="🔙")
else:
    # Load scraped data
    df = pd.DataFrame(st.session_state.scraped_data)

    # Extract numeric values if not already in DataFrame
    if "numeric_price" not in df.columns:
        def extract_numeric(text):
            if not text:
                return 0
            num = ''.join(c for c in text if c.isdigit() or c == '.')
            try:
                return float(num)
            except:
                return 0

        df["numeric_price"] = df["price"].apply(extract_numeric)
        df["numeric_reviews"] = df["reviews"].apply(extract_numeric)

    # Add dummy source label (eBay for now)
    df["source"] = "eBay"

    # Shorten long titles
    df["short_title"] = df["title"].apply(lambda x: x[:40] + "..." if len(x) > 40 else x)

    # Price comparison bar chart
    st.subheader("💵 Price Comparison Bar Chart")
    fig = px.bar(df, x="short_title", y="numeric_price", color="source", barmode="group",
                 labels={"short_title": "Product", "numeric_price": "Price (USD)"},
                 title="Price Comparison (eBay)")
    fig.update_layout(xaxis_tickangle=45, height=600)
    st.plotly_chart(fig, use_container_width=True)

    # Box plot of price distribution
    st.subheader("📦 Price Distribution Box Plot")
    fig2 = px.box(df, x="source", y="numeric_price", color="source",
                  title="Price Distribution by Source")
    st.plotly_chart(fig2, use_container_width=True)
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
