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


bu_prices = []
api_prices = []
selenium_prices = []
api_3d_data=[]
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

except Exception as e:
    st.error(f"An error occurred while accessing SerpAPI: {e}")

st.subheader("📌 Enhanced Network Insights")

if G and G.number_of_nodes() > 0:
    degree_dict = dict(G.degree())
    sorted_degrees = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)
    top_nodes = sorted_degrees[:5]
    st.write("🔝 Top 5 Most Connected Nodes:")
    for node, degree in top_nodes:
        st.markdown(f"- **{node}** with degree `{degree}`")

    communities = list(nx.connected_components(G))
    st.write(f"🌐 Detected **{len(communities)} communities** in the network.")

st.subheader("🤖Scraping using Selenium")
search_query = st.text_input("Enter what you want to search on eBay:")
if search_query:
    search_url = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}&_sop=12"
    driver = webdriver.Chrome()
    driver.get(search_url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "s-item__wrapper"))
        )

        items = driver.find_elements(By.CLASS_NAME, "s-item__wrapper")
        s_data = []
        for item in items:
            try:
                title = item.find_element(By.CLASS_NAME, "s-item__title").text
                price = item.find_element(By.CLASS_NAME, "s-item__price").text
                reviews = "0 reviews"
                try:
                    reviews = item.find_element(By.CLASS_NAME, "clipped").text
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

st.subheader("🔥Heatmap: Price Comparison (BeautifulSoup, API, Selenium)")

def kde_quartic(d, h):
    """
    Quartic Kernel function: returns intensity if distance <= h, else 0.
    """
    dn = d / h
    return (15/16) * (1 - dn**2)**2 if dn <= 1 else 0
points = []
for p in bu_prices:
    try:
        val = float(p.replace("$", "").replace(",", ""))
        val = val if val<200 else 0
        points.append((val, 0))
    except:
        pass
    
for p in api_prices:
    if p is not None:
        p = p if p<200 else 0
        points.append((p, 1))
for p in selenium_prices:
    try:
        val = float(p.replace("$", "").replace(",", ""))
        val = val if val<200 else 0
        points.append((val, 2))
    except:
        pass

if points:
    x = [pt[0] for pt in points] 
    y = [pt[1] for pt in points]

    grid_size = 1
    h = 2 

    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)

    x_grid = np.arange(x_min - h, x_max + h, grid_size/2)
    y_grid = np.arange(y_min - h, y_max + h, grid_size/2)
    x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)
    
    xc = x_mesh + (grid_size/4)
    yc = y_mesh + (grid_size/4)

    intensity_list = []
    for r in range(xc.shape[0]):
        intensity_row = []
        for c in range(xc.shape[1]):
            kde_value_list = []
            for i in range(len(x)):
                d = math.sqrt((xc[r][c] - x[i])**2 + (yc[r][c] - y[i])**2)
                p = kde_quartic(d, h)
                kde_value_list.append(p)
            intensity_row.append(sum(kde_value_list))
        intensity_list.append(intensity_row)
    intensity = np.array(intensity_list)
    plt.figure(figsize=(10, 6))
    hm = plt.pcolormesh(x_mesh, y_mesh, intensity)
    plt.scatter(x, y, c='red', marker='o', label='Data Points', edgecolor='k', s=50)
    plt.colorbar(hm, label='Intensity')
    plt.xlabel("Price")
    
    y_ticks = [0, 1, 2]
    plt.ylabel("Scraping Method")
    plt.yticks(y_ticks, ['BS', 'API', 'Selenium'])
    
    plt.title("KDE Heatmap: Price Distribution by Method")
    plt.legend(loc='upper right')
    st.pyplot(plt)

    plt.savefig("price_heatmap.jpg")
    plt.clf() 
else:
    st.write("Insufficient data to generate heatmap.")
# Streamlit UI
st.subheader("displays a 3D plot.")
# Display a button to fetch and display products
if st.button("Fetch Products"):
    with st.spinner("Fetching products..."):
        products =api_3d_data
        
        # Create a DataFrame from the fetched products
        df = pd.DataFrame(products)

        # Show the product data in a table
        # 3D Plot: Price vs Review Count vs Rating
        st.subheader("3D Visualization of Products (Price, Reviews, Rating)")

        # Clean and convert data types before plotting
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

        # Extract digits from reviews (e.g., "1,200 reviews" → 1200)
        df['reviews'] = pd.to_numeric(df['reviews'].astype(str).str.replace(',', '').str.extract(r'(\d+)')[0], errors='coerce')

        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

        # Drop rows where any of the 3D values are missing
        df = df.dropna(subset=['price', 'reviews', 'rating'])

        # Extracting numeric columns for plotting
        x = df['price']
        y = df['reviews']
        z = df['rating']


        # Plotting the 3D graph
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Scatter plot in 3D
        ax.scatter(x, y, z, c=z, cmap='viridis', marker='o')

        # Labels for axes
        ax.set_xlabel('Price ($)')
        ax.set_ylabel('Reviews')
        ax.set_zlabel('Rating')

        # Title
        ax.set_title(f'3D Visualization of Products')

        # Display the 3D plot
        st.pyplot(fig)