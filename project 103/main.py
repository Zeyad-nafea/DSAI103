import streamlit as st

st.title("🗂️ DSAI 103 Project")

st.markdown("### 📘 Web Scraping using BeautifulSoup")
st.markdown(
    "This section demonstrates basic HTML scraping from eBay using **BeautifulSoup**, "
    "targeting listings, prices, and review info based on a static query (e.g., 'watches for men')."
)
st.page_link("pages/bu.py", label="BeautifulSoup", icon="📁")

st.markdown("### 🕹️ Web Scraping using Selenium")
st.markdown(
    "Here we use **Selenium WebDriver** to automate a browser session, scrape live search results "
    "from eBay based on user input, and extract dynamic data like titles, prices, and reviews."
)
st.page_link("pages/sel.py", label="Selenium", icon="📄",disabled=True)

st.markdown("### 🔑 API-based Data Collection with SerpAPI")
st.markdown(
    "This section leverages **SerpAPI** to fetch structured eBay data using a dedicated API. "
    "It retrieves titles, prices, ratings, reviews, and item links with better accuracy and speed."
)
st.page_link("pages/api.py", label="SerpAPI", icon="📁")

st.markdown("### 📊 Visualizations & Analysis")
st.markdown(
    "Explore various product insights using **Network Graphs (NetworkX)** for relationship modeling, "
    "**Heatmaps** for price comparison across scraping methods, and **3D Plots** for multi-feature views."
)
st.page_link("pages/networkx.py", label="Network Graph", icon="🌐")
st.page_link("pages/heatmap.py", label="Price Heatmap", icon="🔥")
st.page_link("pages/3d.py", label="3D Visualization", icon="🧊")

st.markdown("### 🎬 Project Wrap-Up")
st.markdown(
    "Final acknowledgments, team members, and project reflections including feedback and LinkedIn links."
)
st.page_link("pages/the_end.py", label="End", icon="📼")
