import streamlit as st
import requests

API_URL = "https://nibblepy-api.onrender.com/snippets"

st.set_page_config(page_title="NibblePy", page_icon="🐍")

st.title("NibblePy – Learn Python One Snippet at a Time", anchor=False)

# Fetch data
try:
    response = requests.get(API_URL)
    response.raise_for_status()
    snippets = response.json()  # Expecting a list of snippet dicts
except Exception:
    st.error("Failed to fetch snippets from the API.")
    st.stop()

# Sidebar filters
categories = sorted({snip.get("category") or "Uncategorized" for snip in snippets})
difficulties = sorted({snip.get("difficulty") or "Unknown" for snip in snippets})

selected_category = st.sidebar.selectbox("📂 Filter by Category", ["All"] + categories)
selected_difficulty = st.sidebar.selectbox("🎯 Filter by Difficulty", ["All"] + difficulties, index=1)
query = st.sidebar.text_input("🔍 Search snippets by keyword:", placeholder="'list' or 'class'")

with st.sidebar:
    st.divider()
    st.markdown("""
    <div style='text-align: justify; font-size: 0.9em; margin-bottom: 1rem;'>
        <b>NibblePy</b> is a Streamlit-based web app that lets learners discover Python fundamentals through 
        small, well-explained code examples. Designed for the 'doers' who need practical, bite-sized code snippets
        that produce instant results.
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div style='text-align: left; font-size: 0.9em; margin-bottom: 1rem;'>
        Created by <a href='https://github.com/piotr-daniel' target='_blank'>Piotr Daniel</a> <br>
        <a href='https://github.com/NibblePy/nibblepy-app' target='_blank'>GitHub Repo</a> |
        <a href='https://github.com/NibblePy/nibblepy-api' target='_blank'>NibblePy API</a>
    </div>
    """, unsafe_allow_html=True)


def matches(snippet):
    if selected_category != "All" and (snippet.get("category") or "Uncategorized") != selected_category:
        return False
    if selected_difficulty != "All" and (snippet.get("difficulty") or "Unknown") != selected_difficulty:
        return False
    if query:
        q = query.lower()
        return (
            q in snippet.get("title", "").lower()
            or q in snippet.get("explanation", "").lower()
            or q in snippet.get("code", "").lower()
        )
    return True


filtered_snippets = [snip for snip in snippets if matches(snip)]

if filtered_snippets:
    st.info(f"Showing **{len(filtered_snippets)}** snippet(s) matching your filters")
else:
    st.warning("**None** of the snippets matched your filters")

for snippet in filtered_snippets:
    st.subheader(snippet.get("title", "Untitled"))
    st.code(snippet.get("code", ""), language="python")
    st.markdown(f"**Explanation:** {snippet.get('explanation', 'No explanation provided.')}")
    st.markdown(f"**Difficulty:** `{snippet.get('difficulty', 'Unknown').capitalize()}`")
    st.divider()
