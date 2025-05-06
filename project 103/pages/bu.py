import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
bu_prices = []
st.subheader("🍵Web Scraping by beutiful soup.")
URL = "https://www.ebay.com/sch/i.html?_nkw=watches+for+men&_sop=12"
r = requests.get(URL, verify=False)
soup = BeautifulSoup(r.content, 'html5lib')
items = soup.find_all("div", class_="s-item__wrapper clearfix")
scraped_data = []
for item in items:
    a = item.find('div', class_="s-item__info clearfix")
    if a:
        title_element = a.find('div', class_="s-item__title")
        price_element = a.find('div', class_="s-item__detail s-item__detail--primary")
        reviews_element = a.find('div', class_="s-item__reviews")

        title = title_element.text if title_element else "No title"
        price = price_element.text if price_element else None
        bu_prices.append(price)
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
df_scraped = pd.DataFrame(scraped_data)
st.dataframe(df_scraped)
csv = df_scraped.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="beautiful soup data.csv",
    mime="text/csv",
    icon=":material/download:",
)
st.session_state.bu_prices = bu_prices
st.session_state.scraped_data = scraped_data
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
