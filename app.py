import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load data
df = pd.read_csv("metadata.csv")
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df_clean = df.dropna(subset=['title', 'publish_time'])

st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers")

# Interactive year range filter
year_range = st.slider("Select year range", int(df_clean['year'].min()), int(df_clean['year'].max()), (2020, 2021))
df_filtered = df_clean[(df_clean['year'] >= year_range[0]) & (df_clean['year'] <= year_range[1])]

# Publications by year
year_counts = df_filtered['year'].value_counts().sort_index()
st.bar_chart(year_counts)

# Top journals
top_journals = df_filtered['journal'].value_counts().head(10)
st.bar_chart(top_journals)

# Word cloud for titles
text = " ".join(df_filtered['title'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

st.image(wordcloud.to_array(), use_column_width=True)

# Show sample data
st.dataframe(df_filtered.head())
