import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="YouTube Statistics 2023", layout="wide")

# Title
st.title("🌍 Global YouTube Statistics Dashboard (2023)")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Global YouTube Statistics.csv", encoding="ISO-8859-1")

df = load_data()
df.dropna(subset=["subscribers", "video views", "Country", "category"], inplace=True)

# Sidebar filters
st.sidebar.header("Filter Data")
country_filter = st.sidebar.multiselect("Select Country", sorted(df["Country"].unique()))
category_filter = st.sidebar.multiselect("Select Category", sorted(df["category"].unique()))

filtered_df = df.copy()
if country_filter:
    filtered_df = filtered_df[filtered_df["Country"].isin(country_filter)]
if category_filter:
    filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]

# KPI Section
st.markdown("## 📊 Key Performance Indicators")
col1, col2, col3 = st.columns(3)
col1.metric("Total Channels", len(filtered_df))
col2.metric("Total Subscribers", f"{filtered_df['subscribers'].sum():,}")
col3.metric("Total Video Views", f"{filtered_df['video views'].sum():,}")

# Chart 1: Top 10 YouTubers
st.markdown("### 🎬 Top 10 YouTubers by Subscribers")
top10 = filtered_df.sort_values(by="subscribers", ascending=False).head(10)
fig1 = px.bar(top10, x="Youtuber", y="subscribers", color="subscribers", text="subscribers", color_continuous_scale="Blues")
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Pie Chart for Category
st.markdown("### 📁 Top Categories by Total Subscribers")
cat_df = filtered_df.groupby("category")["subscribers"].sum().sort_values(ascending=False).head(10)
fig2 = px.pie(names=cat_df.index, values=cat_df.values, hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Choropleth Map
st.markdown("### 🗺️ Country-wise Total Subscribers")
country_data = filtered_df.groupby("Country")["subscribers"].sum().reset_index()
fig3 = px.choropleth(country_data, locations="Country", locationmode="country names", color="subscribers", color_continuous_scale="YlGnBu")
st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Bubble Chart
st.markdown("### 🔵 Subscribers vs. Views (Bubble Chart)")
fig4 = px.scatter(filtered_df, x="subscribers", y="video views", size="uploads", color="category", hover_name="Youtuber", log_x=True, log_y=True)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit and Plotly")