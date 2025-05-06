import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D  
api_3d_data = st.session_state.get('api_3d_data', None)
st.subheader("displays a 3D plot.")
if st.button("Fetch Products"):
    with st.spinner("Fetching products..."):
        products =api_3d_data
        
        df = pd.DataFrame(products)

        st.subheader("3D Visualization of Products (Price, Reviews, Rating)")

        df['price'] = pd.to_numeric(df['price'], errors='coerce')

        df['reviews'] = pd.to_numeric(df['reviews'].astype(str).str.replace(',', '').str.extract(r'(\d+)')[0], errors='coerce')

        df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

        df = df.dropna(subset=['price', 'reviews', 'rating'])

        x = df['price']
        y = df['reviews']
        z = df['rating']


        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(x, y, z, c=z, cmap='viridis', marker='o')

        ax.set_xlabel('Price ($)')
        ax.set_ylabel('Reviews')
        ax.set_zlabel('Rating')

        ax.set_title(f'3D Visualization of Products')
        st.pyplot(fig)
        st.page_link("main.py", label="🔙 Return to Main Page", icon="🏠")
