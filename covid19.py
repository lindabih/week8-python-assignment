# CORD-19 Data Analysis Assignment
# Author: Linda Bih
# Date: 2025-09-15

# ------------------------------
# Part 0: Import Libraries
# ------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import streamlit as st

# Optional for nicer plots
sns.set(style="whitegrid")

# ------------------------------
# Part 1: Data Loading and Exploration
# ------------------------------

# Load dataset
df = pd.read_csv("metadata.csv")

# Explore the data
print("Shape of dataset:", df.shape)
print("\nData Types and Non-Null Counts:\n", df.info())
print("\nFirst 5 rows:\n", df.head())
print("\nMissing Values:\n", df.isnull().sum())
print("\nBasic Statistics:\n", df.describe())

# ------------------------------
# Part 2: Data Cleaning and Preparation
# ------------------------------

# Convert publication date to datetime
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# Extract publication year
df['year'] = df['publish_time'].dt.year

# Handle missing values: drop rows without title or publish_time
df_clean = df.dropna(subset=['title', 'publish_time']).copy()

# Create new column: abstract word count
df_clean['abstract_word_count'] = df_clean['abstract'].fillna('').apply(lambda x: len(x.split()))

# Verify cleaning
print("\nAfter Cleaning, Shape:", df_clean.shape)
print(df_clean[['title', 'publish_time', 'year', 'abstract_word_count']].head())

# ------------------------------
# Part 3: Data Analysis and Visualization
# ------------------------------

# 3.1 Publications by Year
year_counts = df_clean['year'].value_counts().sort_index()
plt.figure(figsize=(10,5))
sns.barplot(x=year_counts.index, y=year_counts.values, palette="viridis")
plt.title("Publications by Year")
plt.xlabel("Year")
plt.ylabel("Number of Publications")
plt.show()

# 3.2 Top 10 Journals
top_journals = df_clean['journal'].value_counts().head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="magma")
plt.title("Top 10 Journals Publishing COVID-19 Research")
plt.xlabel("Number of Publications")
plt.ylabel("Journal")
plt.show()

# 3.3 Word Cloud of Paper Titles
text = " ".join(df_clean['title'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

plt.figure(figsize=(15,7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Word Cloud of Paper Titles")
plt.show()

# 3.4 Distribution of Paper Counts by Source
if 'source_x' in df_clean.columns:
    source_counts = df_clean['source_x'].value_counts().head(10)
    plt.figure(figsize=(10,5))
    sns.barplot(x=source_counts.values, y=source_counts.index, palette="coolwarm")
    plt.title("Top Sources of Papers")
    plt.xlabel("Number of Papers")
    plt.ylabel("Source")
    plt.show()

# ------------------------------
# Part 4: Streamlit App
# ------------------------------
# Save this part in a separate file: app.py
# Run with: streamlit run app.py

"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load and clean data
df = pd.read_csv("metadata.csv")
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df_clean = df.dropna(subset=['title', 'publish_time']).copy()

st.title("CORD-19 Data Explorer")
st.write("Interactive exploration of COVID-19 research papers")

# Year range slider
year_range = st.slider("Select publication year range",
                       int(df_clean['year'].min()), int(df_clean['year'].max()),
                       (2020, 2021))
df_filtered = df_clean[(df_clean['year'] >= year_range[0]) & (df_clean['year'] <= year_range[1])]

# Plot Publications by Year
year_counts = df_filtered['year'].value_counts().sort_index()
st.bar_chart(year_counts)

# Top 10 Journals
top_journals = df_filtered['journal'].value_counts().head(10)
st.bar_chart(top_journals)

# Word Cloud for Titles
text = " ".join(df_filtered['title'].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
st.image(wordcloud.to_array(), use_column_width=True)

# Display sample data
st.subheader("Sample Papers")
st.dataframe(df_filtered[['title', 'journal', 'year']].head(10))
"""

# ------------------------------
# Part 5: Documentation and Reflection
# ------------------------------

# Suggested:
# - Add comments explaining each step
# - Write README.md describing dataset, steps, and insights
# - Push your Jupyter Notebook and app.py to GitHub
