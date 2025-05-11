import streamlit as st
import pandas as pd
from serpapi import GoogleSearch

st.set_page_config(page_title="Walmart Scraper", layout="wide")
st.subheader("🛒 Scraping Walmart with SerpAPI")

# Input for search query
search_query = st.text_input("Enter what to search:")

# Replace with your SerpAPI key
API_KEY = "your_serpapi_key"  # Replace this with your SerpAPI key

if search_query:
    # Setup SerpAPI parameters
    params = {
        "q": search_query,
        "location": "United States",  # Optional: you can specify the location
        "device": "desktop",  # Desktop results
        "api_key": API_KEY,
        "engine": "walmart",
        "hl": "en",
    }

    # Call SerpAPI to get results
    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract the product data
    if 'products' in results:
        scraped_data = []
        for product in results['products']:
            title = product.get("title", "No title available")
            price = product.get("price", "No price available")
            url = product.get("url", "No URL available")
            image = product.get("image", "No image available")
            scraped_data.append({
                "title": title,
                "price": price,
                "URL": url,
                "image": image
            })

        # Convert to DataFrame
        df_scraped = pd.DataFrame(scraped_data)

        # Display the DataFrame in Streamlit
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
    else:
        st.error("No products found or API error.")
else:
    st.info("Enter a search term to begin scraping.")
