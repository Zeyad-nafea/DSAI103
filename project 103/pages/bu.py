import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd

st.set_page_config(page_title="Product Scraper", layout="wide")
st.subheader("🍵 Web Scraping with BeautifulSoup (eBay & Amazon)")

# Input
search_query = st.text_input("Enter what to search:")

if search_query:
    scraped_data = []

    # Scrape eBay
    eBay_URL = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}&_sop=12"
    eBay_r = requests.get(eBay_URL, verify=False)
    eBay_soup = BeautifulSoup(eBay_r.content, 'html5lib')
    eBay_items = eBay_soup.find_all("li", class_="s-item")

    for item in eBay_items:
        img_element = item.find('img', class_="s-item__image-img")
        a = item.find('div', class_="s-item__info")

        if a:
            title_element = a.find('h3', class_="s-item__title")
            price_element = a.find('span', class_="s-item__price")

            title = title_element.text.strip() if title_element else "No title"
            price = price_element.text.strip() if price_element else None
            image_url = img_element['src'] if img_element and 'src' in img_element.attrs else None

            scraped_data.append({
                "title": title,
                "price": price,
                "image": image_url,
                "category": "eBay"
            })

    # Scrape Amazon (Note: might be blocked due to scraping prevention)
    amazon_URL = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}"
    amazon_r = requests.get(amazon_URL, headers={'User-Agent': 'Mozilla/5.0'}, verify=False)
    amazon_soup = BeautifulSoup(amazon_r.content, 'html5lib')
    amazon_items = amazon_soup.find_all("div", class_="s-main-slot s-result-list s-search-results sg-row")

    for item in amazon_items:
        img_element = item.find('img', class_="s-image")
        title_element = item.find('span', class_="a-text-normal")
        price_element = item.find('span', class_="a-price-whole")

        if title_element and price_element:
            title = title_element.text.strip() if title_element else "No title"
            price = price_element.text.strip() if price_element else None
            image_url = img_element['src'] if img_element and 'src' in img_element.attrs else None

            scraped_data.append({
                "title": title,
                "price": price,
                "image": image_url,
                "category": "Amazon"
            })

    # Convert price to numeric for sorting
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

    # Add sorting options for price
    sort_by = st.selectbox("Sort products by:", ["None", "Price (Low to High)", "Price (High to Low)"])

    # Apply sorting
    if sort_by == "Price (Low to High)":
        scraped_data = sorted(scraped_data, key=lambda x: x["numeric_price"])
    elif sort_by == "Price (High to Low)":
        scraped_data = sorted(scraped_data, key=lambda x: x["numeric_price"], reverse=True)

    # Convert to DataFrame
    df_scraped = pd.DataFrame(scraped_data)

    # Display in loop with images
    st.markdown("### 🛒 Scraped Products")
    for idx, row in df_scraped.iterrows():
        with st.container():
            cols = st.columns([1, 3])
            if row["image"]:
                cols[0].image(row["image"], width=100)
            else:
                cols[0].write("No Image")
            cols[1].markdown(f"""
                **{row['title']}**  
                💰 {row['price']}  
                🛒 Category: {row['category']}
            """)
            st.markdown("---")

    # CSV download
    csv = df_scraped.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="scraped_data.csv",
        mime="text/csv",
        icon="📥"
    )

    # Store in session state
    st.session_state.scraped_data = scraped_data

    st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
else:
    st.info("Enter a search term above to begin scraping.")
