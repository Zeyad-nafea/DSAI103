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
from mpl_toolkits.mplot3d import Axes3D  # 3D plotting

st.subheader("🔥 Heatmap: Price Comparison (BeautifulSoup & API Only)")

api_prices = st.session_state.get('api_prices', None)
bu_prices = st.session_state.get('bu_prices', None)

if api_prices and bu_prices:
    def kde_quartic(d, h):
        dn = d / h
        return (15/16) * (1 - dn**2)**2 if dn <= 1 else 0

    points = []
    for p in bu_prices:
        try:
            val = float(p.replace("$", "").replace(",", ""))
            if val < 200:
                points.append((val, 0))
        except:
            continue

    for p in api_prices:
        try:
            if p is not None and p < 200:
                points.append((p, 1))
        except:
            continue

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

        xc = x_mesh + (grid_size / 4)
        yc = y_mesh + (grid_size / 4)

        intensity_list = []
        for r in range(xc.shape[0]):
            intensity_row = []
            for c in range(xc.shape[1]):
                kde_values = []
                for i in range(len(x)):
                    d = math.sqrt((xc[r][c] - x[i])**2 + (yc[r][c] - y[i])**2)
                    kde_values.append(kde_quartic(d, h))
                intensity_row.append(sum(kde_values))
            intensity_list.append(intensity_row)

        intensity = np.array(intensity_list)

        fig, ax = plt.subplots(figsize=(10, 6))
        cmap = sns.color_palette("coolwarm", as_cmap=True)
        heat = ax.pcolormesh(x_mesh, y_mesh, intensity, cmap=cmap, shading='auto')

        scatter = ax.scatter(x, y, c='black', edgecolor='white', s=70, label='Prices')
        ax.set_xlabel("Price ($)", fontsize=12)
        ax.set_ylabel("Scraping Method", fontsize=12)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['BeautifulSoup', 'SerpAPI'])
        ax.set_title("💹 KDE Heatmap: Price Distribution", fontsize=14, weight='bold')
        ax.grid(True, linestyle='--', alpha=0.4)

        cbar = plt.colorbar(heat, ax=ax, label="Density (KDE Intensity)")
        ax.legend(loc='upper right')

        st.pyplot(fig)

    else:
        st.warning("❗ Not enough data to generate the heatmap.")
else:
    st.warning("❗ Session state missing data. Please perform scraping first.")

# Return to main page
st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
