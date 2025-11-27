import streamlit as st
import requests

# --- CONFIGURATION ---
# 1. PASTE YOUR KEYS HERE (Keep these secret!)
API_KEY = "PASTE_YOUR_GOOGLE_API_KEY_HERE"
SEARCH_ENGINE_ID = "PASTE_YOUR_CX_ID_HERE"

st.set_page_config(page_title="NyayaSetu Live", page_icon="⚖️")

# --- CUSTOM CSS (To make it look like an App) ---
st.markdown("""
    <style>
    .law-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF9933;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .law-title { font-size: 18px; font-weight: bold; color: #000080; }
    .law-snippet { font-size: 14px; color: #444; margin-top: 5px; }
    .source-tag { font-size: 11px; background-color: #eee; padding: 2px 6px; border-radius: 4px; color: #666; }
    a { text-decoration: none; }
    </style>
""", unsafe_allow_html=True)

# --- FUNCTIONS ---
def google_search(query):
    """Fetches results from Google Custom Search JSON API"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'num': 10  # Number of results (Max 10 per request)
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- APP INTERFACE ---
st.title("⚖️ NyayaSetu Live")
st.caption("Search directly from Indian Kanoon & India Code")

# Search Bar
query = st.text_input("Enter any legal topic (e.g. 'Section 302 IPC', 'Divorce rules'):")

if st.button("Search Google"):
    if not query:
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Searching Indian Law Database..."):
            data = google_search(query)

            # Check for Errors (like invalid API Key)
            if "error" in data:
                if isinstance(data['error'], dict): # Google Error format
                    st.error(f"Google Error: {data['error'].get('message', 'Unknown Error')}")
                else:
                    st.error(f"Connection Error: {data['error']}")
            
            # Check for Results
            elif "items" in data:
                st.success(f"Found {len(data['items'])} results for '{query}'")
                
                for item in data["items"]:
                    title = item.get("title", "No Title")
                    link = item.get("link", "#")
                    snippet = item.get("snippet", "No details available.")
                    source = item.get("displayLink", "google.com")

                    # Display Card
                    st.markdown(f"""
                        <div class="law-card">
                            <div class="law-title"><a href="{link}" target="_blank">{title}</a></div>
                            <div class="law-snippet">{snippet}</div>
                            <br>
                            <span class="source-tag">Source: {source}</span>
                            <a href="{link}" target="_blank" style="float:right; font-size:12px; font-weight:bold; color:#FF9933;">Read Full Text &rarr;</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No results found. Try a specific section number.")

# Footer
st.markdown("---")
st.caption("Powered by Google Programmable Search Engine")
