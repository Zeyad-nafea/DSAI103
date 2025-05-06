import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns

st.subheader("🔥 KDE Heatmap & Colored Block Heatmap: Price Comparison (BeautifulSoup & API only)")

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
            val = val if val < 200 else 0
            points.append((val, 0))
        except:
            pass

    for p in api_prices:
        if p is not None:
            try:
                p = float(p)
                p = p if p < 200 else 0
                points.append((p, 1))
            except:
                pass

    if points:
        x = [pt[0] for pt in points]
        y = [pt[1] for pt in points]

        # KDE Heatmap
        grid_size = 1
        h = 2

        x_min, x_max = min(x), max(x)
        y_min, y_max = min(y), max(y)

        x_grid = np.arange(x_min - h, x_max + h, grid_size / 2)
        y_grid = np.arange(y_min - h, y_max + h, grid_size / 2)
        x_mesh, y_mesh = np.meshgrid(x_grid, y_grid)

        xc = x_mesh + (grid_size / 4)
        yc = y_mesh + (grid_size / 4)

        intensity_list = []
        for r in range(xc.shape[0]):
            intensity_row = []
            for c in range(xc.shape[1]):
                kde_value_list = []
                for i in range(len(x)):
                    d = math.sqrt((xc[r][c] - x[i]) ** 2 + (yc[r][c] - y[i]) ** 2)
                    p = kde_quartic(d, h)
                    kde_value_list.append(p)
                intensity_row.append(sum(kde_value_list))
            intensity_list.append(intensity_row)
        intensity = np.array(intensity_list)

        # Plot KDE Heatmap
        fig1 = plt.figure(figsize=(10, 5))
        hm = plt.pcolormesh(x_mesh, y_mesh, intensity, shading='auto', cmap="plasma")
        plt.scatter(x, y, c='red', marker='o', label='Data Points', edgecolor='k', s=50)
        plt.colorbar(hm, label='Intensity')
        plt.xlabel("Price")
        plt.ylabel("Scraping Method")
        plt.yticks([0, 1], ['BeautifulSoup', 'API'])
        plt.title("🎯 KDE Heatmap: Price Distribution")
        plt.legend(loc='upper right')
        st.pyplot(fig1)
        plt.clf()

        # Colored Block Heatmap using seaborn
        def clean(prices):
            cleaned = []
            for p in prices:
                try:
                    if isinstance(p, str):
                        p = float(p.replace("$", "").replace(",", ""))
                    if p < 200:
                        cleaned.append(p)
                except:
                    continue
            return cleaned

        clean_bu = clean(bu_prices)
        clean_api = clean(api_prices)

        df = pd.DataFrame({
            'BeautifulSoup': pd.Series(clean_bu),
            'API': pd.Series(clean_api)
        })

        df.fillna(df.mean(), inplace=True)

        fig2 = plt.figure(figsize=(12, 2))
        sns.heatmap(df.T, cmap="coolwarm", annot=True, fmt=".1f", linewidths=0.5, cbar=True)
        plt.title("🧱 Colored Block Heatmap: Price Comparison")
        st.pyplot(fig2)
        plt.clf()

    else:
        st.warning("Insufficient data to generate heatmaps.")
else:
    st.info("Please load data into session_state to view heatmaps.")

st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
