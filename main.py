import streamlit as st
import requests

# --- 1. YOUR KEYS ---
API_KEY = "AIzaSyCQsFY0H2At4z0yW8LpFAnaty6gcpiAcQM"
SEARCH_ENGINE_ID = "d7bd9ba85538f492c"

st.set_page_config(page_title="NyayaSetu Live", page_icon="⚖️")

# --- 2. MULTI-LANGUAGE CONFIGURATION ---
# This dictionary holds the translations and search logic
LANGUAGES = {
    "English": {
        "title": "⚖️ NyayaSetu",
        "caption": "Indian Laws Direct Search",
        "ph": "Enter Topic or Section...",
        "buttons": ["🏠 Family", "👮 Crime", "💼 Business", "📢 Rights"],
        "suffix": "" # No suffix for English
    },
    "Hindi": {
        "title": "⚖️ न्याय-सेतु",
        "caption": "भारतीय कानून - सीधी खोज",
        "ph": "विषय या धारा दर्ज करें...",
        "buttons": ["🏠 परिवार", "👮 अपराध", "💼 व्यापार", "📢 अधिकार"],
        "suffix": " in Hindi" # We add this to the search to get Hindi results
    },
    "Kannada": {
        "title": "⚖️ ನ್ಯಾಯ ಸೇತುವೆ",
        "caption": "ಭಾರತೀಯ ಕಾನೂನುಗಳ ಹುಡುಕಾಟ",
        "ph": "ವಿಷಯ ಅಥವಾ ವಿಭಾಗವನ್ನು ನಮೂದಿಸಿ...",
        "buttons": ["🏠 ಕುಟುಂಬ", "👮 ಅಪರಾಧ", "💼 ವ್ಯಾಪಾರ", "📢 ಹಕ್ಕುಗಳು"],
        "suffix": " in Kannada"
    },
    "Tamil": {
        "title": "⚖️ நியாய சேது",
        "caption": "இந்திய சட்டங்கள் தேடல்",
        "ph": "தலைப்பு அல்லது பிரிவை உள்ளிடவும்...",
        "buttons": ["🏠 குடும்பம்", "👮 குற்றம்", "💼 வணிகம்", "📢 உரிமைகள்"],
        "suffix": " in Tamil"
    },
    "Telugu": {
        "title": "⚖️ న్యాయ సేతు",
        "caption": "భారతీయ చట్టాల శోధన",
        "ph": "అంశం లేదా విభాగం నమోదు చేయండి...",
        "buttons": ["🏠 కుటుంబం", "👮 నేరం", "💼 వ్యాపారం", "📢 హక్కులు"],
        "suffix": " in Telugu"
    }
}

# --- 3. STYLE (CSS) ---
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
    .stButton>button { width: 100%; border-radius: 8px; border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR LANGUAGE SELECTOR ---
st.sidebar.header("Language / भाषा")
selected_lang = st.sidebar.selectbox("Choose Language:", list(LANGUAGES.keys()))
text = LANGUAGES[selected_lang] # Get the dictionary for the chosen language

# --- 5. GOOGLE SEARCH FUNCTION ---
def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'num': 10
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- 6. APP LAYOUT ---
st.title(text["title"])
st.caption(text["caption"])

# --- BRANCHES (Dynamic based on Language) ---
st.write("---")
cols = st.columns(4)

# When a button is clicked, we set the query AND append the language suffix
if cols[0].button(text["buttons"][0]): # Family
    st.session_state['q'] = "Hindu Marriage Act Divorce Section 13" + text["suffix"]
if cols[1].button(text["buttons"][1]): # Crime
    st.session_state['q'] = "BNS Section 303 Theft Punishment" + text["suffix"]
if cols[2].button(text["buttons"][2]): # Business
    st.session_state['q'] = "Section 138 Negotiable Instruments Act Cheque Bounce" + text["suffix"]
if cols[3].button(text["buttons"][3]): # Rights
    st.session_state['q'] = "Consumer Protection Act 2019 rights" + text["suffix"]

# --- SEARCH BAR ---
default_value = st.session_state.get('q', "")
# We strip the suffix for display so the user sees clean text, but we add it back during search
display_value = default_value.replace(text["suffix"], "") 

user_query = st.text_input(text["ph"], value=display_value)

# --- EXECUTE SEARCH ---
if st.button("Search"):
    if not user_query:
        st.warning("Please type something first.")
    else:
        # Combine User Input + Language Suffix (e.g., "Theft" + " in Hindi")
        final_query = user_query + text["suffix"]
        
        with st.spinner(f"Searching in {selected_lang}..."):
            data = google_search(final_query)

            if "error" in data:
                error_msg = data['error'].get('message', str(data['error']))
                if "API key" in error_msg:
                    st.error("❌ API Key Error. Check Google Cloud Console.")
                else:
                    st.error(f"Error: {error_msg}")
            
            elif "items" in data:
                st.success(f"Found {len(data['items'])} results")
                for item in data["items"]:
                    title = item.get('title', 'No Title')
                    link = item.get('link', '#')
                    snippet = item.get('snippet', 'No details.')
                    source = item.get('displayLink', 'Source')

                    st.markdown(f"""
                        <div class="law-card">
                            <div class="law-title"><a href="{link}" target="_blank">{title}</a></div>
                            <div class="law-snippet">{snippet}</div>
                            <br>
                            <span class="source-tag">{source}</span>
                            <a href="{link}" target="_blank" style="float:right; color:#FF9933; font-weight:bold;">Read &rarr;</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No results found. Try simpler words.")
