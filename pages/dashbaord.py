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

# ------------------------
# Additional Plotly Charts (5+ neat and clean plots)
# ------------------------

st.subheader("🗺️ World GDP Choropleth (2025)")
try:
    fig = px.choropleth(df, locations='Country', locationmode='country names', color='2025',
                        color_continuous_scale='Plasma', title='World GDP (2025) — Choropleth')
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**Insight:** A geographic view of 2025 GDP highlights regional concentrations of economic size.")
except Exception as e:
    st.warning(f"Choropleth could not be rendered: {e}")


st.subheader("🔬 GDP vs Growth Scatter (2025 vs Growth % 2020-2025)")
df_scatter = df_growth.copy()
df_scatter['GDP_2025_M'] = df_scatter['2025']
fig = px.scatter(df_scatter, x='GDP_2025_M', y='Growth %', hover_name='Country',
                 color='Growth %', color_continuous_scale='Turbo',
                 title='GDP (2025) vs Growth % (2020→2025)')
fig.update_layout(xaxis_title='GDP (2025, Millions USD)', yaxis_title='Growth % (2020→2025)')
st.plotly_chart(fig)
st.markdown("**Insight:** Compare the size of an economy to its growth rate; watch out for small but fast-growing economies.")


st.subheader("📊 Correlation Heatmap (Years 2020–2025)")
years = ['2020','2021','2022','2023','2024','2025']
corr = df[years].corr()
fig = px.imshow(corr, text_auto=True, color_continuous_scale='Viridis',
                title='Correlation of GDP between Years (2020–2025)')
fig.update_layout(width=800, height=500)
st.plotly_chart(fig)
st.markdown("**Insight:** Shows how consistent country rankings and magnitudes are across years.")


st.subheader("📦 GDP Distribution by Year (Box Plot)")
fig = px.box(df_melted, x='Year', y='GDP', points='outliers', color='Year',
             title='GDP Distribution Across Countries by Year')
st.plotly_chart(fig)
st.markdown("**Insight:** Compare spread and outliers of GDP each year.")


st.subheader("📈 Distribution of GDP (2025) — Histogram")
fig = px.histogram(df, x='2025', nbins=30, marginal='box',
                   title='Distribution of GDP in 2025 (per country)')
fig.update_layout(xaxis_title='GDP (2025, Millions USD)', yaxis_title='Count of Countries')
st.plotly_chart(fig)
st.markdown("**Insight:** Understand how GDPs are distributed in 2025; many countries cluster at lower values.")
