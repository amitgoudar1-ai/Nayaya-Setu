import streamlit as st
import requests

# --- 1. SAFELY IMPORT TRANSLATOR ---
try:
    from deep_translator import GoogleTranslator
    HAS_TRANSLATOR = True
except ImportError:
    HAS_TRANSLATOR = False

# --- 2. YOUR KEYS ---
API_KEY = "AIzaSyCQsFY0H2At4z0yW8LpFAnaty6gcpiAcQM"
SEARCH_ENGINE_ID = "d7bd9ba85538f492c"

st.set_page_config(page_title="NyayaSetu", page_icon="⚖️", layout="centered", initial_sidebar_state="collapsed")

# --- HIDE STREAMLIT BRANDING (New Code) ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;} /* Hides the hamburger menu */
            footer {visibility: hidden;}    /* Hides 'Made with Streamlit' */
            header {visibility: hidden;}    /* Hides the top header bar */
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 3. MULTI-LANGUAGE CONFIGURATION ---
LANGUAGES = {
    "English": {"code": "en", "title": "⚖️ NyayaSetu", "caption": "Indian Laws Direct Search", "ph": "Enter Topic...", "buttons": ["🏠 Family", "👮 Crime", "💼 Business", "📢 Rights"], "suffix": ""},
    "Hindi": {"code": "hi", "title": "⚖️ न्याय-सेतु", "caption": "भारतीय कानून - सीधी खोज", "ph": "विषय दर्ज करें...", "buttons": ["🏠 परिवार", "👮 अपराध", "💼 व्यापार", "📢 अधिकार"], "suffix": " in Hindi"},
    "Kannada": {"code": "kn", "title": "⚖️ ನ್ಯಾಯ ಸೇತುವೆ", "caption": "ಭಾರತೀಯ ಕಾನೂನುಗಳ ಹುಡುಕಾಟ", "ph": "ವಿಷಯವನ್ನು ನಮೂದಿಸಿ...", "buttons": ["🏠 ಕುಟುಂಬ", "👮 ಅಪರಾಧ", "💼 ವ್ಯಾಪಾರ", "📢 ಹಕ್ಕುಗಳು"], "suffix": " in Kannada"},
    "Tamil": {"code": "ta", "title": "⚖️ நியாய சேது", "caption": "இந்திய சட்டங்கள் தேடல்", "ph": "தலைப்பை உள்ளிடவும்...", "buttons": ["🏠 குடும்பம்", "👮 குற்றம்", "💼 வணிகம்", "📢 உரிமைகள்"], "suffix": " in Tamil"},
    "Telugu": {"code": "te", "title": "⚖️ న్యాయ సేతు", "caption": "భారతీయ చట్టాల శోధన", "ph": "అంశం నమోదు చేయండి...", "buttons": ["🏠 కుటుంబం", "👮 నేరం", "💼 వ్యాపారం", "📢 హక్కులు"], "suffix": " in Telugu"}
}

# --- 4. CSS STYLES ---
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

# --- 5. FUNCTIONS ---
def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {'key': API_KEY, 'cx': SEARCH_ENGINE_ID, 'q': query, 'num': 10}
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def safe_translate(text_content, target_lang):
    if HAS_TRANSLATOR and target_lang != "en":
        try:
            return GoogleTranslator(source='auto', target=target_lang).translate(text_content)
        except:
            return text_content
    return text_content

# --- 6. APP LAYOUT ---

# Top Language Selector
st.caption("Select Language / भाषा चुनें:")
selected_lang = st.selectbox("", list(LANGUAGES.keys()), label_visibility="collapsed")
text = LANGUAGES[selected_lang]

st.title(text["title"])
st.caption(text["caption"])

if not HAS_TRANSLATOR:
    st.info("⚠️ Note: Translation tool is installing. Results will be in English for a moment.")

# Branches
st.write("---")
cols = st.columns(4)
if cols[0].button(text["buttons"][0]): st.session_state['q'] = "Hindu Marriage Act Divorce Section 13" + text["suffix"]
if cols[1].button(text["buttons"][1]): st.session_state['q'] = "BNS Section 303 Theft Punishment" + text["suffix"]
if cols[2].button(text["buttons"][2]): st.session_state['q'] = "Section 138 Negotiable Instruments Act Cheque Bounce" + text["suffix"]
if cols[3].button(text["buttons"][3]): st.session_state['q'] = "Consumer Protection Act 2019 rights" + text["suffix"]

# Search
default_val = st.session_state.get('q', "").replace(text["suffix"], "")
user_query = st.text_input(text["ph"], value=default_val)

if st.button("Search"):
    if not user_query:
        st.warning("Please type something.")
    else:
        final_query = user_query + text["suffix"]
        with st.spinner(f"Searching..."):
            data = google_search(final_query)
            
            if "items" in data:
                st.success(f"Found {len(data['items'])} results")
                for item in data["items"]:
                    title = item.get('title', '')
                    snippet = item.get('snippet', '')
                    link = item.get('link', '#')
                    source = item.get('displayLink', '')

                    title = safe_translate(title, text["code"])
                    snippet = safe_translate(snippet, text["code"])

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
