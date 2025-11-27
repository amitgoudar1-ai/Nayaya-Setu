import streamlit as st
import requests
from deep_translator import GoogleTranslator

# --- 1. YOUR KEYS ---
API_KEY = "AIzaSyCQsFY0H2At4z0yW8LpFAnaty6gcpiAcQM"
SEARCH_ENGINE_ID = "d7bd9ba85538f492c"

st.set_page_config(page_title="NyayaSetu Live", page_icon="⚖️")

# --- 2. MULTI-LANGUAGE CONFIGURATION ---
# Added 'code' for translation (ISO 639-1 codes)
LANGUAGES = {
    "English": {
        "code": "en",
        "title": "⚖️ NyayaSetu",
        "caption": "Indian Laws Direct Search",
        "ph": "Enter Topic or Section...",
        "buttons": ["🏠 Family", "👮 Crime", "💼 Business", "📢 Rights"],
        "suffix": "" 
    },
    "Hindi": {
        "code": "hi",
        "title": "⚖️ न्याय-सेतु",
        "caption": "भारतीय कानून - सीधी खोज",
        "ph": "विषय या धारा दर्ज करें...",
        "buttons": ["🏠 परिवार", "👮 अपराध", "💼 व्यापार", "📢 अधिकार"],
        "suffix": " in Hindi"
    },
    "Kannada": {
        "code": "kn",
        "title": "⚖️ ನ್ಯಾಯ ಸೇತುವೆ",
        "caption": "ಭಾರತೀಯ ಕಾನೂನುಗಳ ಹುಡುಕಾಟ",
        "ph": "ವಿಷಯ ಅಥವಾ ವಿಭಾಗವನ್ನು ನಮೂದಿಸಿ...",
        "buttons": ["🏠 ಕುಟುಂಬ", "👮 ಅಪರಾಧ", "💼 ವ್ಯಾಪಾರ", "📢 ಹಕ್ಕುಗಳು"],
        "suffix": " in Kannada"
    },
    "Tamil": {
        "code": "ta",
        "title": "⚖️ நியாய சேது",
        "caption": "இந்திய சட்டங்கள் தேடல்",
        "ph": "தலைப்பு அல்லது பிரிவை உள்ளிடவும்...",
        "buttons": ["🏠 குடும்பம்", "👮 குற்றம்", "💼 வணிகம்", "📢 உரிமைகள்"],
        "suffix": " in Tamil"
    },
    "Telugu": {
        "code": "te",
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
text = LANGUAGES[selected_lang] 

# --- 5. FUNCTIONS ---

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

# New Function: Translate Text
def translate_content(text_content, target_lang):
    try:
        if target_lang == "en": return text_content
        # Use deep_translator to convert text
        return GoogleTranslator(source='auto', target=target_lang).translate(text_content)
    except:
        return text_content # If error, return original text

# --- 6. APP LAYOUT ---
st.title(text["title"])
st.caption(text["caption"])

# --- BRANCHES ---
st.write("---")
cols = st.columns(4)

# When a button is clicked, we set the query AND append the language suffix
if cols[0].button(text["buttons"][0]): 
    st.session_state['q'] = "Hindu Marriage Act Divorce Section 13" + text["suffix"]
if cols[1].button(text["buttons"][1]): 
    st.session_state['q'] = "BNS Section 303 Theft Punishment" + text["suffix"]
if cols[2].button(text["buttons"][2]): 
    st.session_state['q'] = "Section 138 Negotiable Instruments Act Cheque Bounce" + text["suffix"]
if cols[3].button(text["buttons"][3]): 
    st.session_state['q'] = "Consumer Protection Act 2019 rights" + text["suffix"]

# --- SEARCH BAR ---
default_value = st.session_state.get('q', "")
display_value = default_value.replace(text["suffix"], "") 
user_query = st.text_input(text["ph"], value=display_value)

# --- EXECUTE SEARCH ---
if st.button("Search"):
    if not user_query:
        st.warning("Please type something first.")
    else:
        # 1. Search Logic
        final_query = user_query + text["suffix"]
        
        with st.spinner(f"Searching & Translating to {selected_lang}..."):
            data = google_search(final_query)

            if "error" in data:
                st.error("Error connecting to Google.")
            
            elif "items" in data:
                st.success(f"Found {len(data['items'])} results")
                
                # 2. Loop through results
                for item in data["items"]:
                    title = item.get('title', 'No Title')
                    link = item.get('link', '#')
                    snippet = item.get('snippet', 'No details.')
                    source = item.get('displayLink', 'Source')

                    # 3. TRANSLATION MAGIC
                    # If language is NOT English, we translate the title and snippet
                    if text["code"] != "en":
                        title = translate_content(title, text["code"])
                        snippet = translate_content(snippet, text["code"])

                    # 4. Display
                    st.markdown(f"""
                        <div class="law-card">
                            <div class="law-title"><a href="{link}" target="_blank">{title}</a></div>
                            <div class="law-snippet">{snippet}</div>
                            <br>
                            <span class="source-tag">{source}</span>
                            <a href="{link}" target="_blank" style="float:right; color:#FF9933; font-weight:bold;">Read Original &rarr;</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No results found.")
