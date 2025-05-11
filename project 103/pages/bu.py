import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd

st.set_page_config(page_title="Walmart Scraper", layout="wide")
st.subheader("🍵 Web Scraping with BeautifulSoup (Walmart)")

# Input
search_query = st.text_input("Enter what to search:")

if search_query:
    # Initialize lists for scraped data
    scraped_data = []

    # Create Walmart search URL
    URL = f"https://www.walmart.com/search/?query={search_query.replace(' ', '%20')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find product items on the page
    items = soup.find_all("div", class_="search-result-gridview-item-wrapper")

    # Extract product data
    for item in items:
        title_element = item.find("a", class_="product-title-link")
        price_element = item.find("span", class_="price-main")
        img_element = item.find("img", class_="search-result-productimage")
        rating_element = item.find("span", class_="visuallyhidden")
        
        title = title_element.text.strip() if title_element else "No title"
        price = price_element.text.strip() if price_element else "No price"
        img_url = img_element['src'] if img_element else "No image"
        rating = rating_element.text.strip() if rating_element else "No rating"

        scraped_data.append({
            "title": title,
            "price": price,
            "rating": rating,
            "image": img_url
        })

    # Convert to DataFrame
    df_scraped = pd.DataFrame(scraped_data)

    # Display Data
    st.dataframe(df_scraped)

    # CSV download
    csv = df_scraped.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="walmart_scraped_data.csv",
        mime="text/csv",
        icon=":material/download:"
    )

    # Store in session state
    st.session_state.scraped_data = scraped_data

    st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
else:
    st.info("Enter a search term above to begin scraping.")
