import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import requests
import ssl
import seaborn as sns
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context
api_prices = []
st.subheader("🔑APIs: Retrieve structured data using SerpAPI.")
G = None
search_q = st.text_input("Enter what to search:")
api_data = []
api_3d_data=[]
if search_q:
    params = {
        "api_key": "35b14e40f911b494dcd9bb49f9453de5aa432c8b2d823ffc5984d84a8d0b71fa",
        "engine": "ebay",
        "_nkw": search_q,
        "output": "json"
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params, verify=False)
        results = response.json()
        res = results.get("organic_results", [])

        for item in res:
            title = item.get("title", "No title")
            link = item.get("link", "No link")
            price = item.get("price", "No price")
            rating = item.get("rating", "No rating")
            reviews = item.get("reviews", "No reviews")
            rating0= item.get("rating",0)
            reviews0 = item.get("reviews", 0)
            if isinstance(price, dict) and "extracted" in price:
                price_value = price["extracted"]
            elif isinstance(price, str):
                try:
                    price_value = float(price.replace("$", "").replace(",", ""))
                except:
                    price_value = None
            else:
                price_value = None
            api_3d_data.append({
                "price": price_value,
                "rating": rating0,
                "reviews": reviews0,
            })
            api_data.append({
                "title": title,
                "price": price_value,
                "rating": rating,
                "reviews": reviews,
                "link": link
            })
            api_prices.append(price_value)

        df = pd.DataFrame(api_data)
        df.to_csv("watches.csv", index=False)
        st.dataframe(df)
        api_csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download API CSV",
            data=api_csv,
            file_name="api_data.csv",
            mime="text/csv",
            icon=":material/download:",
        )
    except Exception as e:
        st.error(f"An error occurred while accessing SerpAPI: {e}")
st.session_state.api_prices = api_prices
st.session_state.api_data = api_data 
st.session_state.api_3d_data = api_3d_data