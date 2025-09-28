import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------
# Page Config
# ------------------------
st.set_page_config(page_title="Global GDP Dashboard", page_icon="🌍", layout="wide")

# ------------------------
# Load Dataset
# ------------------------
df = pd.read_csv('2020-2025.csv')
df_melted = df.melt(id_vars="Country", var_name="Year", value_name="GDP")

# ------------------------
# Sidebar Filters
# ------------------------
st.sidebar.title("Filters & Options")
selected_year = st.sidebar.selectbox("Select Year", ["2020","2021","2022","2023","2024","2025"])
selected_countries = st.sidebar.multiselect("Select Countries", df["Country"].unique(), default=df["Country"].unique()[:10])
top_n = st.sidebar.slider("Top N Economies", min_value=5, max_value=20, value=10)



# ------------------------
# Dynamic Key Metrics for Selected Year
# ------------------------
st.subheader(f"📊 Key Metrics for {selected_year}")

# Total GDP
total_gdp = df[selected_year].sum()

# Highest GDP
highest_idx = df[selected_year].idxmax()
highest_country = df.loc[highest_idx, "Country"]
highest_value = df.loc[highest_idx, selected_year]

# Lowest GDP
lowest_idx = df[selected_year].idxmin()
lowest_country = df.loc[lowest_idx, "Country"]
lowest_value = df.loc[lowest_idx, selected_year]

col1, col2, col3 = st.columns(3)
col1.metric(f"🌐 Total Global GDP ({selected_year})", f"${total_gdp:,.0f}M")
col2.metric(f"💰 Highest GDP Country ({selected_year})", f"{highest_country} (${highest_value:,.0f}M)")
col3.metric(f"📉 Lowest GDP Country ({selected_year})", f"{lowest_country} (${lowest_value:,.0f}M)")

# ------------------------
# GDP Trend - Top N Economies
# ------------------------
st.subheader(f"📈 GDP Trend of Top {top_n} Economies (2020-2025)")
top_countries = df.nlargest(top_n, "2025")["Country"]
fig = px.line(df_melted[df_melted["Country"].isin(top_countries)], x="Year", y="GDP", color="Country",
              title=f"GDP Trend of Top {top_n} Economies")
st.plotly_chart(fig)
st.markdown("**Insight:** This graph shows the growth trajectory of top economies over 6 years.")

# ------------------------
# GDP Trend - Selected Countries
# ------------------------
st.subheader("📊 GDP Trend for Selected Countries")
fig = px.line(df_melted[df_melted["Country"].isin(selected_countries)], x="Year", y="GDP", color="Country",
              title="GDP Trend of Selected Countries")
st.plotly_chart(fig)
st.markdown("**Insight:** Allows comparison of GDP trends for countries of interest.")

# ------------------------
# GDP Comparison - 2020 vs 2025
# ------------------------
st.subheader("🔁 GDP Comparison: 2020 vs 2025")
fig = go.Figure(data=[
    go.Bar(name='2020', x=df['Country'], y=df['2020']),
    go.Bar(name='2025', x=df['Country'], y=df['2025'])
])
fig.update_layout(barmode='group', title="GDP Comparison: 2020 vs 2025")
st.plotly_chart(fig)
st.markdown("**Conclusion:** Identify which countries improved or declined in GDP over the 6-year period.")

# ------------------------
# Animated GDP Ranking
# ------------------------
st.subheader("🎞 Animated GDP Ranking Over Years")
fig = px.bar(df_melted, x="GDP", y="Country", color="Country", orientation="h",
             animation_frame="Year", title="GDP Ranking Over 2020–2025")
st.plotly_chart(fig)
st.markdown("**Insight:** Watch how country rankings change over time.")

# ------------------------
# GDP Growth Rate (%) - Bar Chart
# ------------------------
st.subheader("🌡 GDP Growth Rate (%) 2020-2025")
df_growth = df.copy()
df_growth["Growth %"] = ((df_growth["2025"] - df_growth["2020"]) / df_growth["2020"]) * 100
fig = px.bar(df_growth.sort_values("Growth %", ascending=False),
             x="Country", y="Growth %",
             color="Growth %",
             color_continuous_scale="Viridis",
             title="GDP Growth Rate (%) from 2020 to 2025")
st.plotly_chart(fig)
st.markdown("**Conclusion:** Green indicates fast-growing economies, red indicates slow growth or decline.")

# ------------------------
# Pie Chart - World GDP Share 2025
# ------------------------
st.subheader("🥧 World GDP Share (2025)")
fig = px.pie(df, names="Country", values="2025", title="World GDP Share (2025)")
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)
st.markdown("**Insight:** Visualize the proportion of global GDP contributed by each country.")

# ------------------------
# Treemap - GDP 2025
# ------------------------
st.subheader("🌳 GDP Treemap (2025)")
fig = px.treemap(df, path=["Country"], values="2025", title="GDP Treemap (2025)")
st.plotly_chart(fig)
st.markdown("**Conclusion:** Quickly identify the largest economies and their relative sizes.")
