import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from bs4 import BeautifulSoup
import requests
import ssl
import urllib3
import certifi
import math
import seaborn as sns
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

st.subheader("🤖Scraping using Selenium")
search_query = st.text_input("Enter what you want to search on eBay:")

if search_query:
    search_url = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}&_sop=12"
    
    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Start driver with webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(search_url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "s-item__wrapper"))
        )
        items = driver.find_elements(By.CLASS_NAME, "s-item__wrapper")
        s_data = []
        selenium_prices = []
        for item in items[2:]:
            try:
                title = item.find_element(By.CLASS_NAME, "s-item__title").text
                price = item.find_element(By.CLASS_NAME, "s-item__price").text
                reviews = "0 reviews"
                try:
                    reviews = item.find_element(By.CLASS_NAME, "s-item__reviews-count").text
                except:
                    pass
                selenium_prices.append(price)
                s_data.append({
                    "title": title,
                    "price": price,
                    "reviews": reviews,
                    "category": search_query.capitalize()
                })

            except Exception as e:
                print("Error processing item:", e)
        df = pd.DataFrame(s_data)
        st.dataframe(df)
        s_csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Selenium CSV",
            data=s_csv,
            file_name="selenium data.csv",
            mime="text/csv",
            icon=":material/download:",
        )
    finally:
        driver.quit()
    
    st.session_state.selenium_prices = selenium_prices
    st.session_state.s_data = s_data
