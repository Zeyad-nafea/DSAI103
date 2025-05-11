import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd

st.set_page_config(page_title="eBay Scraper", layout="wide")
st.subheader("🍵 Web Scraping with BeautifulSoup (eBay)")

# Input
search_query = st.text_input("Enter what to search:")

if search_query:
    bu_prices = []
    scraped_data = []

    # Create eBay search URL
    URL = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}&_sop=12"
    r = requests.get(URL, verify=False)
    soup = BeautifulSoup(r.content, 'html5lib')
    items = soup.find_all("div", class_="s-item__wrapper clearfix")

    # Extract item data
    for item in items:
        a = item.find('div', class_="s-item__info clearfix")
        if a:
            title_element = a.find('div', class_="s-item__title")
            price_element = a.find('div', class_="s-item__detail s-item__detail--primary")
            reviews_element = a.find('div', class_="s-item__reviews")

            title = title_element.text if title_element else "No title"
            price = price_element.text if price_element else None
            reviews = "0"
            if reviews_element:
                reviews_span = reviews_element.find('span', class_="clipped")
                if reviews_span:
                    reviews = reviews_span.text

            scraped_data.append({
                "title": title,
                "price": price,
                "reviews": reviews,
                "category": "watches"
            })
            bu_prices.append(price)

    # Convert price/reviews to numeric for sorting
    def extract_numeric(text):
        if not text:
            return 0
        num = ''.join(c for c in text if c.isdigit() or c == '.')
        try:
            return float(num)
        except:
            return 0

    for product in scraped_data:
        product["numeric_price"] = extract_numeric(product["price"])
        product["numeric_reviews"] = extract_numeric(product["reviews"])

    # Add sorting options
    sort_by = st.selectbox("Sort products by:", ["None", "Price (Low to High)", "Price (High to Low)", "Reviews (High to Low)"])

    # Apply sorting
    if sort_by == "Price (Low to High)":
        scraped_data = sorted(scraped_data, key=lambda x: x["numeric_price"])
    elif sort_by == "Price (High to Low)":
        scraped_data = sorted(scraped_data, key=lambda x: x["numeric_price"], reverse=True)
    elif sort_by == "Reviews (High to Low)":
        scraped_data = sorted(scraped_data, key=lambda x: x["numeric_reviews"], reverse=True)

    # Convert to DataFrame
    df_scraped = pd.DataFrame(scraped_data)

    # Display
    st.dataframe(df_scraped)

    # CSV download
    csv = df_scraped.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="beautiful_soup_data.csv",
        mime="text/csv",
        icon=":material/download:"
    )

    # Store in session state
    st.session_state.bu_prices = bu_prices
    st.session_state.scraped_data = scraped_data

    st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
else:
    st.info("Enter a search term above to begin scraping.")
