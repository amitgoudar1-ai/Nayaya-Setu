import streamlit as st
import requests

# --- 1. SAFELY IMPORT TRANSLATOR ---
# This prevents crashes if the library is missing
try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

# --- 2. YOUR KEYS (Already Inserted) ---
API_KEY = "AIzaSyCQsFY0H2At4z0yW8LpFAnaty6gcpiAcQM"
SEARCH_ENGINE_ID = "d7bd9ba85538f492c"

# --- 3. PAGE CONFIG ---
st.set_page_config(page_title="NyayaSetu", page_icon="⚖️", layout="centered", initial_sidebar_state="collapsed")

# --- 4. HIDE STREAMLIT BRANDING (Footer & Menu) ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 5. MULTI-LANGUAGE CONFIGURATION ---
LANGUAGES = {
    "English": {"code": "en", "title": "⚖️ NyayaSetu", "caption": "Indian Laws Direct Search", "ph": "Enter Topic...", "buttons": ["🏠 Family", "👮 Crime", "💼 Business", "📢 Rights"], "suffix": ""},
    "Hindi": {"code": "hi", "title": "⚖️ न्याय-सेतु", "caption": "भारतीय कानून - सीधी खोज", "ph": "विषय दर्ज करें...", "buttons": ["🏠 परिवार", "👮 अपराध", "💼 व्यापार", "📢 अधिकार"], "suffix": " in Hindi"},
    "Kannada": {"code": "kn", "title": "⚖️ ನ್ಯಾಯ ಸೇತುವೆ", "caption": "ಭಾರತೀಯ ಕಾನೂನುಗಳ ಹುಡುಕಾಟ", "ph": "ವಿಷಯವನ್ನು ನಮೂದಿಸಿ...", "buttons": ["🏠 ಕುಟುಂಬ", "👮 ಅಪರಾಧ", "💼 ವ್ಯಾಪಾರ", "📢 ಹಕ್ಕುಗಳು"], "suffix": " in Kannada"},
    "Tamil": {"code": "ta", "title": "⚖️ நியாய சேது", "caption": "இந்திய சட்டங்கள் தேடல்", "ph": "தலைப்பை உள்ளிடவும்...", "buttons": ["🏠 குடும்பம்", "👮 குற்றம்", "💼 வணிகம்", "📢 உரிமைகள்"], "suffix": " in Tamil"},
    "Telugu": {"code": "te", "title": "⚖️ న్యాయ సేతు", "caption": "భారతీయ చట్టాల శోధన", "ph": "అంశం నమోదు చేయండి...", "buttons": ["🏠 కుటుంబం", "👮 నేరం", "💼 వ్యాపారం", "📢 హక్కులు"], "suffix": " in Telugu"}
}

# --- 6. CSS STYLES (For Cards & Buttons) ---
st.markdown("""
    <style>
    .law-card { background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #FF9933; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; }
    .law-title { font-size: 18px; font-weight: bold; color: #000080; }
    .law-snippet { font-size: 14px; color: #444; margin-top: 5px; }
    .source-tag { font-size: 11px; background-color: #eee; padding: 2px 6px; border-radius: 4px; color: #666; }
    a { text-decoration: none; }
    .stButton>button { width: 100%; border-radius: 8px; border: 1px solid #ddd; }
    </style>
""", unsafe_allow_html=True)

# --- 7. FUNCTIONS ---
def google_search(query):
    """Connects to Google Custom Search API"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {'key': API_KEY, 'cx': SEARCH_ENGINE_ID, 'q': query, 'num': 10}
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def safe_translate(text_content, target_lang):
    """Translates text if tool is available"""
    if HAS_TRANSLATOR and target_lang != "en":
        try:
            return GoogleTranslator(source='auto', target=target_lang).translate(text_content)
        except:
            return text_content
    return text_content

# --- 8. APP LAYOUT ---

# Top Language Selector
st.caption("Select Language / भाषा चुनें:")
selected_lang = st.selectbox("", list(LANGUAGES.keys()), label_visibility="collapsed")
text = LANGUAGES[selected_lang]

st.title(text["title"])
st.caption(text["caption"])

if not HAS_TRANSLATOR:
    st.info("⚠️ Translation tool is installing. Results in English for now.")

# Branches
st.write("---")
cols = st.columns(4)
# Note: We append the suffix so Google knows which language to search for
if cols[0].button(text["buttons"][0]): st.session_state['q'] = "Hindu Marriage Act Divorce Section 13" + text["suffix"]
if cols[1].button(text["buttons"][1]): st.session_state['q'] = "BNS Section 303 Theft Punishment" + text["suffix"]
if cols[2].button(text["buttons"][2]): st.session_state['q'] = "Section 138 Negotiable Instruments Act Cheque Bounce" + text["suffix"]
if cols[3].button(text["buttons"][3]): st.session_state['q'] = "Consumer Protection Act 2019 rights" + text["suffix"]

# Search Bar
# Remove suffix for display so user sees clean text
default_val = st.session_state.get('q', "").replace(text["suffix"], "")
user_query = st.text_input(text["ph"], value=default_val)

# Execute Search
if st.button("Search"):
    if not user_query:
        st.warning("Please type something.")
    else:
        final_query = user_query + text["suffix"]
        with st.spinner(f"Searching..."):
            data = google_search(final_query)
            
            # Handle API Errors
            if "error" in data:
                err_msg = str(data['error'])
                if "key" in err_msg.lower():
                    st.error("❌ API Key Error. Check Google Cloud Console.")
                else:
                    st.error(f"Error: {err_msg}")
            
            # Handle Success
            elif "items" in data:
                st.success(f"Found {len(data['items'])} results")
                for item in data["items"]:
                    title = item.get('title', '')
                    snippet = item.get('snippet', '')
                    link = item.get('link', '#')
                    source = item.get('displayLink', '')

                    # Translate the result
                    title = safe_translate(title, text["code"])
                    snippet = safe_translate(snippet, text["code"])

                    # Display Card
                    st.markdown(f"""
                        <div class="law-card">
                            <div class="law-title"><a href="{link}" target="_blank">{title}</a></div>
                            <div class="law-snippet">{snippet}</div>
                            <span class="source-tag">{source}</span>
                            <a href="{link}" target="_blank" style="float:right; color:#FF9933; font-weight:bold;">Read &rarr;</a>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No results found.")
