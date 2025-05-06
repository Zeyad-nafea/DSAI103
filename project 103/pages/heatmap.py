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
from mpl\_toolkits.mplot3d import Axes3D  # 3D plotting

st.subheader("🔥Heatmap: Price Comparison (BeautifulSoup & API only)")
api\_prices = st.session\_state.get('api\_prices', None)
bu\_prices = st.session\_state.get('bu\_prices', None)

if api\_prices and bu\_prices:
def kde\_quartic(d, h):
"""
Quartic Kernel function: returns intensity if distance <= h, else 0.
"""
dn = d / h
return (15/16) \* (1 - dn\*\*2)\*\*2 if dn <= 1 else 0

```
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
        p = p if p < 200 else 0
        points.append((p, 1))

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
    
    y_ticks = [0, 1]
    plt.ylabel("Scraping Method")
    plt.yticks(y_ticks, ['BS', 'API'])
    
    plt.title("KDE Heatmap: Price Distribution by Method")
    plt.legend(loc='upper right')
    st.pyplot(plt)

    plt.savefig("price_heatmap.jpg")
    plt.clf() 
else:
    st.write("Insufficient data to generate heatmap.")
```

else:
st.write("Insufficient data to generate heatmap.")
st.page\_link("main.py", label="🔙 Return to Main Page", icon="🏠") 
