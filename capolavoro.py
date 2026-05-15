import streamlit as st
import pandas as pd

# --- CONFIG & STYLES ---
st.set_page_config(page_title="OMNILINGUA", layout="wide") 

BANNER_URL = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #050517; }}
    
    .block-container {{
        background-color: #0d0d2b; 
        max-width: 850px !important; 
        padding: 0 2rem 2rem 2rem !important; 
        box-shadow: 0 0 50px rgba(0,0,0,0.5); 
        margin-top: 20px;
        margin-bottom: 40px;
        border-radius: 20px;
    }}
    
    .banner {{
        width: calc(100% + 4rem); 
        margin-left: -2rem;
        height: 250px;
        background-image: linear-gradient(to bottom, rgba(13, 13, 43, 0.3), rgba(13, 13, 43, 1)), url('{BANNER_URL}');
        background-size: cover; background-position: center;
        border-radius: 20px 20px 0 0;
    }}
    
    .header-wrapper {{
        width: 100%;
        margin-top: -110px;
        margin-bottom: 40px;
        text-align: center;
        z-index: 1000;
        position: relative;
    }}
    
    .header-title {{ 
        color: white !important; 
        font-family: 'Arial Black', sans-serif; 
        font-size: 65px !important; 
        margin: 0 !important;
        padding: 0 !important;
        text-shadow: 0 5px 25px rgba(0,0,0,0.9);
        letter-spacing: 4px;
        line-height: 1.1;
    }}
    
    .sub-title {{ 
        color: #ffffff; 
        font-size: 16px; 
        margin: 10px 0 0 0 !important;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
        display: block;
        width: 100%;
        text-align: center;
    }}

    div[data-baseweb="input"] {{
        background-color: #1a1a3a !important; border-radius: 15px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        margin-top: 30px;
    }}
    input {{ color: white !important; }}
    
    .rank-card {{
        background-color: #1a1a3a; border-radius: 12px; padding: 10px;
        height: 140px; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        border: 1px solid rgba(255,255,255,0.05);
    }}
    
    .wiki-link {{
        color: #4dabff; 
        text-decoration: none; 
        font-size: 13px; 
        font-style: italic; 
        opacity: 0.7;
    }}
    
    header, footer {{visibility: hidden;}}
    hr {{ border-color: rgba(255,255,255,0.05); margin: 25px 0; }}
    </style>
    
    <div class="banner"></div>

    <div class="header-wrapper">
        <h1 class="header-title">OMNILINGUA</h1>
        <p class="sub-title">discover every language of the world</p>
    </div>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        # Carica il CSV e ordina per il valore numerico 'val'
        data = pd.read_csv("lingue.csv")
        data = data.sort_values(by='val', ascending=False).reset_index(drop=True)
        return data
    except Exception as e:
        st.error(f"Errore caricamento: {e}")
        return None

df_raw = load_data()

if df_raw is not None:
    search = st.text_input("", placeholder="🔍 search language name...").strip()

    if search:
        df = df_raw[df_raw['nome'].str.contains(search, case=False, na=False)]
    else:
        df = df_raw

    if df.empty:
        st.markdown('<div style="text-align:center; padding: 40px; color: #8a8ab0;">No languages found.</div>', unsafe_allow_html=True)
    else:
        for index, row in df.iterrows():
            # Calcolo stelle difficoltà
            try:
                stars_count = int(row['difficolta'])
                stars_html = "<span style='color:#ffd700'>★</span>" * stars_count
            except:
                stars_html = "N/A"
            
            speaker_text = row['speakers']
            learn_link = row['link_learn']
            wiki_url = f"https://en.wikipedia.org/wiki/{row['nome'].replace(' ', '_')}_language"
            
            # Rank basato sulla posizione nel DF ordinato
            display_rank = index + 1

            col1, col2, col3 = st.columns([1.5, 4, 1])
            
            with col1:
                st.markdown(f'''
                    <div class="rank-card">
                        <div style="color: #4dabff; font-size: 11px; font-weight: bold;">RANK</div>
                        <div style="color: white; font-size: 40px; font-weight: bold;">#{display_rank}</div>
                    </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div style="color: white; padding-left: 20px;">
                        <div style="font-size: 26px; font-weight: bold; margin-bottom: 2px;">{row['nome']}</div>
                        <div style="margin-bottom: 10px;">
                            <a href="{wiki_url}" target="_blank" class="wiki-link">
                                📖 Learn more on Wikipedia
                            </a>
                        </div>
                        <div style="font-size: 16px; line-height: 1.8;">
                            <span style="color: #b0b0cc;">Speakers:</span> {speaker_text}<br>
                            <span style="color: #b0b0cc;">Difficulty:</span> {stars_html}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: center; height: 140px;">
                        <a href="{learn_link}" target="_blank" 
                           style="text-decoration:none; background-color: #4dabff; color: white; 
                                  padding: 10px 20px; border-radius: 10px; font-weight: bold; font-size: 14px;">
                           LEARN 🚀
                        </a>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr>", unsafe_allow_html=True)
else:
    st.error("⚠️ 'lingue.csv' non trovato o non valido.")