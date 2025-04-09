import streamlit as st

st.set_page_config(page_title="About the Project", layout="centered")

st.title("📘 About this Fake News Detection Project")

st.markdown("""
### 🤖 Goal

This project aims to detect and classify news articles based on their trustworthiness.  
By leveraging data collected from various sources and running them through an ML model,  
we assign each article one of the following predictions:

- **Fake news**
- **Suspicious news**
- **Trustful news**
- **Real news**

### 🛠 Tech stack

- **RedditAPI** for scraping news articles from [r/worldnews](https://www.reddit.com/r/worldnews/new/)
- **Google Cloud Platform (BigQuery)** for storing and querying large-scale news data
- **Python & FastAPI** for data processing and machine learning
- **Airflow** for orchestrating data pipelines
- **Streamlit** for interactive visualization
- **[GitHub](https://github.com/HadjMohamed/NLP-FakeNews)** for version control and collaboration
- **Scheduled updates every 24h**

### 💡 Why this matters

With the growing spread of misinformation online, this tool helps users visualize how content from different authors and sources is classified, and allows for quick, live access to structured insights.

### 🧑‍💻 Author

Built with ❤️ by four enthusiasts:
- Wissem Abdeljaouad
- Mohamed Hadj 
- Erwann Leletty
- Gauthier Magne
""")
