import streamlit as st
import requests

# --- 1. YOUR KEYS (Already Inserted) ---
API_KEY = "AIzaSyCQsFY0H2At4z0yW8LpFAnaty6gcpiAcQM"
SEARCH_ENGINE_ID = "d7bd9ba85538f492c"

st.set_page_config(page_title="NyayaSetu Live", page_icon="⚖️")

# --- 2. STYLE (CSS) ---
st.markdown("""
    <style>
    .law-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF9933; /* Saffron Border */
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    .law-title { font-size: 18px; font-weight: bold; color: #000080; }
    .law-snippet { font-size: 14px; color: #444; margin-top: 5px; }
    .source-tag { font-size: 11px; background-color: #eee; padding: 2px 6px; border-radius: 4px; color: #666; }
    a { text-decoration: none; }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. GOOGLE SEARCH FUNCTION ---
def google_search(query):
    """Fetches laws using your specific keys"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'num': 10  # Max results per search
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- 4. APP LAYOUT ---
st.title("⚖️ NyayaSetu")
st.caption("Indian Laws Direct Search")

# --- BRANCHES (Quick Access Buttons) ---
st.write("---")
cols = st.columns(4)

# When a button is clicked, we set the search query automatically
if cols[0].button("🏠 Family"):
    st.session_state['q'] = "Hindu Marriage Act Divorce Section 13"
if cols[1].button("👮 Crime"):
    st.session_state['q'] = "BNS Section 303 Theft Punishment"
if cols[2].button("💼 Business"):
    st.session_state['q'] = "Section 138 Negotiable Instruments Act Cheque Bounce"
if cols[3].button("📢 Rights"):
    st.session_state['q'] = "Consumer Protection Act 2019 rights"

# --- SEARCH BAR ---
# It reads from the button click OR user typing
default_value = st.session_state.get('q', "")
query = st.text_input("Enter Topic or Section:", value=default_value)

# --- EXECUTE SEARCH ---
if st.button("Search Law"):
    if not query:
        st.warning("Please type something first.")
    else:
        with st.spinner("Searching official legal databases..."):
            data = google_search(query)

            # --- ERROR HANDLING ---
            if "error" in data:
                error_msg = data['error'].get('message', str(data['error']))
                
                # Check for common errors
                if "API key not valid" in error_msg:
                    st.error("❌ Google Cloud API is not ENABLED. Go to Console > Search 'Custom Search API' > Click ENABLE.")
                elif "Billing" in error_msg:
                    st.error("❌ Billing Error. (Use the free HTML version if this persists).")
                else:
                    st.error(f"Error: {error_msg}")
            
            # --- SUCCESS ---
            elif "items" in data:
                st.success(f"Found {len(data['items'])} results for '{query}'")
                for item in data["items"]:
                    title = item.get('title', 'No Title')
                    link = item.get('link', '#')
                    snippet = item.get('snippet', 'No details.')
                    source = item.get('displayLink', 'Source')

                    # Draw the card
                    st.markdown(f"""
                        <div class="law-card">
                            <div class="law-title"><a href="{link}" target="_blank">{title}</a></div>
                            <div class="law-snippet">{snippet}</div>
                            <br>
                            <span class="source-tag">Source: {source}</span>
                            <a href="{link}" target="_blank" style="float:right; color:#FF9933; font-weight:bold;">Read Full &rarr;</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No results found. Try simpler words like 'Theft' or 'Divorce'.")

