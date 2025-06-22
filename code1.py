import streamlit as st
import json
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# === Page Setup ===
st.set_page_config(page_title="Twitter Sentiment Dashboard", layout="wide")

# === Load JSON Data ===
file_path = "outputjson_twiteerfile.json"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error(f"❌ File not found: {file_path}")
    st.stop()
except json.JSONDecodeError as e:
    st.error(f"❌ JSON decoding failed: {e}")
    st.stop()

if not data:
    st.error("🚫 No data loaded. The file may be empty or invalid.")
    st.stop()

# === Process Records ===
records = []
for item in data:
    try:
        text = item['original'].get('comment') or item['original'].get('text')
        sentiment = item['sentiment']['Sentiment']
        scores = item['sentiment']['SentimentScore']
        records.append({
            "text": text,
            "sentiment": sentiment,
            "positive": scores['Positive'],
            "negative": scores['Negative'],
            "neutral": scores['Neutral'],
            "mixed": scores['Mixed']
        })
    except Exception as e:
        continue

if not records:
    st.error("🚫 No valid records found.")
    st.stop()

df = pd.DataFrame(records)

# === Dashboard Title ===
st.title("📊 Twitter Company Sentiment Analysis Dashboard")

# === Layout ===
col1, col2 = st.columns(2)

# === Donut Chart ===
with col1:
    st.subheader("🧁 Sentiment Donut Chart")
    sentiment_counts = df["sentiment"].value_counts()
    fig_donut = px.pie(
        names=sentiment_counts.index,
        values=sentiment_counts.values,
        hole=0.4,
        color=sentiment_counts.index,
        color_discrete_sequence=px.colors.qualitative.Safe,
        title="Sentiment Distribution"
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# === Heatmap of Sentiment Scores ===
with col2:
    st.subheader("🌡️ Correlation Heatmap")
    fig_heatmap, ax = plt.subplots()
    sns.heatmap(df[["positive", "negative", "neutral", "mixed"]].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig_heatmap)

# === Sentiment Scores Line Chart ===
st.subheader("📈 Sentiment Scores Across Records")
fig_line = px.line(
    df,
    y=["positive", "negative", "neutral", "mixed"],
    labels={"value": "Score", "variable": "Sentiment"},
    title="Sentiment Scores Over Records"
)
st.plotly_chart(fig_line, use_container_width=True)

# === Sentiment Histogram ===
st.subheader("📊 Sentiment Label Histogram")
fig_hist = px.histogram(df, x="sentiment", color="sentiment", title="Sentiment Distribution Histogram")
st.plotly_chart(fig_hist, use_container_width=True)

# === Top Positive and Negative Comments ===
st.subheader("💬 Top Positive & Negative Comments")

top_pos = df.sort_values("positive", ascending=False).head(5)[["text", "positive"]]
top_neg = df.sort_values("negative", ascending=False).head(5)[["text", "negative"]]

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🔝 Top Positive Comments")
    for i, row in top_pos.iterrows():
        st.info(f"✅ {row['text']} ({row['positive']:.2f})")

with col4:
    st.markdown("#### ⚠️ Top Negative Comments")
    for i, row in top_neg.iterrows():
        st.error(f"❌ {row['text']} ({row['negative']:.2f})")

# === Full Data Table ===
st.subheader("🗂️ Full Sentiment Data")
st.dataframe(df)
