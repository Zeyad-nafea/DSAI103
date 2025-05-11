import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd

st.subheader("🍵 Web Scraping with BeautifulSoup (eBay)")

search_q = st.text_input("Enter what to search:")

if search_q:
    bu_prices = []
    scraped_data = []

    URL = f"https://www.ebay.com/sch/i.html?_nkw={search_q.replace(' ', '+')}&_sop=12"
    r = requests.get(URL, verify=False)
    
    soup = BeautifulSoup(r.content, 'html5lib')
    items = soup.find_all("div", class_="s-item__wrapper clearfix")
    
    for item in items[2:]:
        a = item.find('div', class_="s-item__info clearfix")
        if a:
            title_element = a.find('div', class_="s-item__title")
            price_element = a.find('div', class_="s-item__detail s-item__detail--primary")
            reviews_element = a.find('div', class_="s-item__reviews")
            image_element = a.find('img', class_="s-item__image-img")

            title = title_element.text if title_element else "No title"
            price = price_element.text if price_element else None
            reviews = "0"
            if reviews_element:
                reviews_span = reviews_element.find('span', class_="clipped")
                if reviews_span:
                    reviews = reviews_span.text

            image_url = image_element['src'] if image_element else None

            scraped_data.append({
                "title": title,
                "price": price,
                "reviews": reviews,
                "image_url": image_url,
                "category": "watches"
            })
            bu_prices.append(price)

    df_scraped = pd.DataFrame(scraped_data)
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
