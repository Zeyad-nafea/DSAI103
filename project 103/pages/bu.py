import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd

st.subheader("🍵Web Scraping from Multiple Sites (eBay + Amazon)")
search_query = st.text_input("Enter what to search:")

all_data = []

if search_query:
    ## eBay Scraping
    ebay_url = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}&_sop=12"
    ebay_resp = requests.get(ebay_url, verify=False)
    ebay_soup = BeautifulSoup(ebay_resp.content, 'html5lib')
    ebay_items = ebay_soup.find_all("div", class_="s-item__wrapper clearfix")
    
    for item in ebay_items:
        a = item.find('div', class_="s-item__info clearfix")
        if a:
            title_element = a.find('div', class_="s-item__title")
            price_element = a.find('div', class_="s-item__detail s-item__detail--primary")
            reviews_element = a.find('div', class_="s-item__reviews")

            title = title_element.text if title_element else "No title"
            price = price_element.text if price_element else "N/A"
            reviews = "0"
            if reviews_element:
                reviews_span = reviews_element.find('span', class_="clipped")
                if reviews_span:
                    reviews = reviews_span.text

            all_data.append({
                "title": title,
                "price": price,
                "reviews": reviews,
                "source": "eBay"
            })

    ## Amazon Scraping (simplified demo — real scraping needs headers and may be blocked)
    amazon_url = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    amazon_resp = requests.get(amazon_url, headers=headers)
    amazon_soup = BeautifulSoup(amazon_resp.content, "html.parser")
    amazon_items = amazon_soup.find_all("div", {"data-component-type": "s-search-result"})

    for item in amazon_items[:10]:  # Limit to 10 items to keep it fast
        title = item.h2.text if item.h2 else "No title"
        price_whole = item.find("span", class_="a-price-whole")
        price_frac = item.find("span", class_="a-price-fraction")
        price = f"${price_whole.text}.{price_frac.text}" if price_whole and price_frac else "N/A"
        reviews = item.find("span", class_="a-icon-alt")
        reviews = reviews.text if reviews else "0 reviews"

        all_data.append({
            "title": title,
            "price": price,
            "reviews": reviews,
            "source": "Amazon"
        })

    # Displaying
    df_all = pd.DataFrame(all_data)
    st.dataframe(df_all)

    csv = df_all.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Combined CSV",
        data=csv,
        file_name="scraped_products.csv",
        mime="text/csv",
        icon=":material/download:",
    )
