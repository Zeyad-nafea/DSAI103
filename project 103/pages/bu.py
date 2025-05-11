import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
bu\_prices = \[]
st.subheader("🍵Web Scraping by beutiful soup.")
search\_q = st.text\_input("Enter what to search:")
URL = f"[https://www.ebay.com/sch/i.html?\_nkw={search\_query.replace(](https://www.ebay.com/sch/i.html?_nkw={search_query.replace%28)' ', '+')}&*sop=12"
r = requests.get(URL, verify=False)
soup = BeautifulSoup(r.content, 'html5lib')
items = soup.find\_all("div", class*="s-item\_\_wrapper clearfix")
scraped\_data = \[]
for item in items:
a = item.find('div', class\_="s-item\_\_info clearfix")
if a:
title\_element = a.find('div', class\_="s-item\_\_title")
price\_element = a.find('div', class\_="s-item\_\_detail s-item\_\_detail--primary")
reviews\_element = a.find('div', class\_="s-item\_\_reviews")

```
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
```

df\_scraped = pd.DataFrame(scraped\_data)
st.dataframe(df\_scraped)
csv = df\_scraped.to\_csv(index=False).encode("utf-8")
st.download\_button(
label="Download CSV",
data=csv,
file\_name="beautiful soup data.csv",
mime="text/csv",
icon="\:material/download:",
)
st.session\_state.bu\_prices = bu\_prices
st.session\_state.scraped\_data = scraped\_data
st.page\_link("main.py", label="🔙 Return to Main Page", icon="🏠")
