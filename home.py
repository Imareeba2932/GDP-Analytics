import streamlit as st

# ------------------------
# Page Config
# ------------------------
st.set_page_config(page_title="Global GDP Dashboard", page_icon="🌍", layout="wide")

# ------------------------
# Banner Image
# ------------------------
st.image("https://png.pngtree.com/png-vector/20220720/ourmid/pngtree-rising-global-gdp-and-investment-prices-during-economic-rebound-vector-png-image_32806224.jpg",
         use_container_width=True)



# ------------------------
# Title & Intro
# ------------------------
st.title("🌍 Global GDP Dashboard (2020-2025)")
st.markdown("""
Welcome to the **Global GDP Analysis Dashboard**!  

Here you can explore:  
- 📈 **GDP Trends** of countries over the years  
- 🔁 **Ranking Changes** from 2020 to 2025  
- 🌡 **Growth Rate Analysis**  
- 🥧 **Global GDP Share & Treemaps**  

Use the **sidebar** to filter countries, years, or top N economies and get interactive insights.  
""")

# ------------------------
# Key Highlights / Cards
# ------------------------
col1, col2, col3 = st.columns(3)

col1.markdown("""
<div style="background-color:#4CAF50; padding:20px; border-radius:10px; text-align:center;">
<h3 style="color:white">🌐 Total Countries</h3>
<p style="color:white; font-size:20px">196</p>
</div>
""", unsafe_allow_html=True)

col2.markdown("""
<div style="background-color:#2196F3; padding:20px; border-radius:10px; text-align:center;">
<h3 style="color:white">💰 Highest GDP</h3>
<p style="color:white; font-size:20px">USA</p>
</div>
""", unsafe_allow_html=True)

col3.markdown("""
<div style="background-color:#FF5722; padding:20px; border-radius:10px; text-align:center;">
<h3 style="color:white">📉 Lowest GDP</h3>
<p style="color:white; font-size:20px">Tuvalu</p>
</div>
""", unsafe_allow_html=True)
