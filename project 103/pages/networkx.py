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
from mpl_toolkits.mplot3d import Axes3D  # 3D plotting
api_data = st.session_state.get('api_data', None)
st.subheader("Network Graph Visualization")
def categorize_price(price):
     if price < 50:
            return "$0-50"
     elif price < 100:
            return "$50-100"
     elif price < 200:
            return "$100-200"
     elif price < 500:
            return "$200-500"
     else:
            return "$500+"
        
def categorize_reviews(reviews):
     try:
         if isinstance(reviews, str):
                reviews_value = int(reviews.replace(',', '').split()[0])
         elif isinstance(reviews, int):
                 reviews_value = reviews
         else:
                 return "Unknown Reviews"
     except (TypeError, ValueError):
                 return "Unknown Reviews"
     if reviews_value < 10:
                return "0-10 reviews"
     elif reviews_value < 50:
                return "10-50 reviews"
     elif reviews_value < 100:
                return "50-100 reviews"
     elif reviews_value < 500:
                return "100-500 reviews"
     else:
                return "500+ reviews"
def create_watch_graph(data):
    G = nx.Graph()
    for watch in data:
        watch_name = watch["title"][:15] 
        price_category = categorize_price(watch["price"])
        reviews_category = categorize_reviews(watch["reviews"])

        G.add_node(watch_name, type="Watch")
        G.add_node(price_category, type="Price")
        G.add_node(reviews_category, type="Reviews")

        G.add_edge(watch_name, price_category)
        G.add_edge(watch_name, reviews_category)

    return G
def draw_graph(G):
            plt.clf()
            pos = nx.spring_layout(G, seed=42)
            node_colors = [
                "cyan" if G.nodes[n]["type"] == "Watch" else (
                    "blue" if G.nodes[n]["type"] == "Price" else "green"
                )
                for n in G.nodes
            ]

            plt.figure(figsize=(12, 8))
            nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="gray", node_size=2000, font_size=8)
            st.pyplot(plt)

filtered_data = [
            watch for watch in api_data
            if watch["title"] and watch["price"] and watch["reviews"]
        ]
G = create_watch_graph(filtered_data)
draw_graph(G)
st.subheader("📌 Enhanced Network Insights")

if G and G.number_of_nodes() > 0:
    degree_dict = dict(G.degree())
    sorted_degrees = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)
    top_nodes = sorted_degrees[:5]
    st.write("🔝 Top 5 Most Connected Nodes:")
    for node, degree in top_nodes:
        st.markdown(f"- **{node}** with degree `{degree}`")
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")

communities = list(nx.connected_components(G))
st.write(f"🌐 Detected **{len(communities)} communities** in the network.")
