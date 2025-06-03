import streamlit as st
import requests

API_URL = "https://nibblepy-api.onrender.com/snippets"

st.set_page_config(page_title="NibblePy", page_icon="🐍")

st.title("NibblePy – Learn Python One Snippet at a Time", anchor=False)

# Fetch data
# noinspection PyBroadException
try:
    response = requests.get(API_URL)
    response.raise_for_status()
    snippets = response.json()
except Exception as e:
    st.error("Failed to fetch snippets from the API.")
    st.stop()

# Sidebar filters
categories = sorted(set(s.get("category", "Uncategorized") for s in snippets.values()))
difficulties = sorted(set(s["difficulty"] for s in snippets.values()))

selected_category = st.sidebar.selectbox("📂 Filter by Category", ["All"] + categories)
selected_difficulty = st.sidebar.selectbox("🎯 Filter by Difficulty", ["All"] + difficulties, index=1)
query = st.sidebar.text_input("🔍 Search snippets by keyword:", placeholder="'list' or 'class'")
with st.sidebar:
    st.divider()
    st.markdown("""
    <div style='text-align: left; font-size: 0.9em; margin-bottom: 1rem;'>
        Created by <a href='https://github.com/piotr-daniel' target='_blank'>Piotr Daniel</a> <br>
        <a href='https://github.com/NibblePy/nibblepy-app' target='_blank'>GitHub Repo</a> |
        <a href='https://github.com/NibblePy/nibblepy-api' target='_blank'>NibblePy API</a>
    </div>
    """, unsafe_allow_html=True)


# Filter snippets
def matches(snippet):
    if selected_category != "All" and snippet.get("category") != selected_category:
        return False
    if selected_difficulty != "All" and snippet["difficulty"] != selected_difficulty:
        return False
    if query:
        q = query.lower()
        return (
                q in snippet["title"].lower()
                or q in snippet["explanation"].lower()
                or q in snippet["code"].lower()
                or any(q in rel.lower() for rel in snippet.get("related", []))
        )
    return True


# Filtered results
filtered_snippets = [snippet for snippet in snippets.values() if matches(snippet)]

# Display result count and snippets
if len(filtered_snippets) > 0:
    st.info(f"Showing **{len(filtered_snippets)}** snippet(s) matching your filters")
elif len(filtered_snippets) == 0:
    st.warning(f"**None** of the snippets has matched your filters")
else:
    st.error(f"An error has occurred, please reset the filter and try again")

if snippets:
    for key, snippet in snippets.items():
        if matches(snippet):
            st.subheader(snippet["title"])
            st.code(snippet["code"], language="python")
            st.markdown(f"**Explanation:** {snippet['explanation']}")
            st.markdown(f"**Difficulty:** `{snippet['difficulty'].capitalize()}`")
            if snippet.get("related"):
                st.markdown(f"**Related:** `{', '.join(snippet['related'])}`")
            st.divider()
