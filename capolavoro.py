import streamlit as st
import pandas as pd

# --- CONFIG & STYLES ---
st.set_page_config(page_title="OMNILINGUA", layout="wide")

BANNER_URL = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop"

st.markdown(f"""
    <style>
    /* Nasconde la barra nera nativa di Streamlit (Share, GitHub, ecc.) */
    [data-testid="stHeader"] {{
        display: none !important;
    }}
    
    /* Rimuove lo spazio vuoto in alto lasciato dalla barra nascosta */
    .stAppDeployDropdown {{
        display: none !important;
    }}
    
    /* Sfondo generale leggermente più chiaro */
    .stApp {{ background-color: #12122c; }} 
    
    .block-container {{
        background-color: #1b1b3a; 
        max-width: 850px !important; 
        padding: 1rem !important; 
        box-shadow: 0 0 50px rgba(0,0,0,0.5); 
        margin-top: 10px;
        border-radius: 20px;
    }}
    
    /* Tendina (Sidebar) della stessa palette di colori */
    [data-testid="stSidebar"] {{
        background-color: #1b1b3a !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #e0e0e0;
    }}

    /* Personalizzazione estetica del tasto Filtra nella sidebar */
    div.stButton > button {{
        background-color: #4dabff !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        width: 100%;
        font-weight: bold;
        padding: 10px;
        transition: background-color 0.3s;
    }}
    div.stButton > button:hover {{
        background-color: #358ecc !important;
        color: white !important;
    }}

    .banner {{
        width: 100%;
        height: 180px;
        background-image: linear-gradient(to bottom, rgba(27, 27, 58, 0), rgba(27, 27, 58, 1)), url('{BANNER_URL}');
        background-size: cover;
        background-position: center;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }}
    
    /* Banner più alto su dispositivi mobili (telefoni) */
    @media (max-width: 768px) {{
        .banner {{
            height: 250px;
        }}
    }}

    .main-title {{
        color: white;
        font-size: clamp(30px, 8vw, 55px);
        font-weight: 800;
        letter-spacing: 3px;
        text-shadow: 0 0 20px rgba(77, 171, 255, 0.8);
        text-align: center;
    }}
    .language-card {{
        background: rgba(255, 255, 255, 0.05); 
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(77, 171, 255, 0.3);
    }}
    .wiki-link {{ color: #4dabff; text-decoration: none; font-weight: bold; font-size: 14px; }}
    </style>
    <div class="banner">
        <div class="main-title">OMNILINGUA</div>
    </div>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_csv('lingue.csv')

try:
    df = load_data()
except FileNotFoundError:
    st.error("Errore: File 'lingue.csv' non trovato. Assicurati che sia nella stessa cartella dello script.")
    st.stop()

# --- INIZIALIZZAZIONE STATE ---
# Usiamo lo st.session_state per salvare i filtri attivi in memoria
if 'search_active' not in st.session_state:
    st.session_state.search_active = ""
if 'diff_active' not in st.session_state:
    st.session_state.diff_active = "Tutte"
if 'sort_by_active' not in st.session_state:
    st.session_state.sort_by_active = "Nome"
if 'sort_dir_active' not in st.session_state:
    st.session_state.sort_dir_active = "↑ Crescente"

# --- SIDEBAR WIDGETS ---
st.sidebar.title("🔍 Filtri")

# I widget cambiano temporaneamente i valori di input...
search_input = st.sidebar.text_input("Cerca una lingua...", value=st.session_state.search_active)

diff_options = ["Tutte", "⭐ 1", "⭐⭐ 2", "⭐⭐⭐ 3", "⭐⭐⭐⭐ 4", "⭐⭐⭐⭐⭐ 5"]
current_diff_idx = diff_options.index(st.session_state.diff_active)
diff_input = st.sidebar.selectbox("Difficoltà", diff_options, index=current_diff_idx)

sort_by_options = ["Nome", "Parlanti", "Difficoltà"]
current_sort_idx = sort_by_options.index(st.session_state.sort_by_active)
sort_by_input = st.sidebar.selectbox("Ordina per", sort_by_options, index=current_sort_idx)

sort_dir_options = ["↑ Crescente", "↓ Decrescente"]
current_dir_idx = sort_dir_options.index(st.session_state.sort_dir_active)
sort_dir_input = st.sidebar.selectbox("Ordine", sort_dir_options, index=current_dir_idx)

# Tasto statico fisso sempre presente
btn_filtra = st.sidebar.button("Applica Filtri 🚀")

# ...ma i filtri cambiano EFFETTIVAMENTE solo quando clicchi il tasto
if btn_filtra:
    st.session_state.search_active = search_input
    st.session_state.diff_active = diff_input
    st.session_state.sort_by_active = sort_by_input
    st.session_state.sort_dir_active = sort_dir_input
    st.rerun()

# --- MAIN LOGIC (Utilizza i filtri salvati nello state) ---
ascending = st.session_state.sort_dir_active == "↑ Crescente"

filtered_df = df[df['nome'].str.contains(st.session_state.search_active, case=False)].copy()

if st.session_state.diff_active != "Tutte":
    exact_diff = diff_options.index(st.session_state.diff_active)  
    filtered_df = filtered_df[filtered_df['difficolta'] == exact_diff]

if st.session_state.sort_by_active == "Nome":
    filtered_df = filtered_df.sort_values('nome', ascending=ascending)
elif st.session_state.sort_by_active == "Difficoltà":
    filtered_df = filtered_df.sort_values('difficolta', ascending=ascending)
elif st.session_state.sort_by_active == "Parlanti":
    def parse_speakers(s):
        s = str(s).lower().replace(',', '.')
        parts = s.split()
        try:
            val = float(''.join(c for c in parts[0] if c.isdigit() or c == '.'))
        except:
            return 0
        if any('miliard' in p for p in parts):
            val *= 1000
        return val
    filtered_df['_spk'] = filtered_df['speakers'].apply(parse_speakers)
    filtered_df = filtered_df.sort_values('_spk', ascending=ascending).drop(columns=['_spk'])

# --- RENDERING DEI RISULTATI ---
if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        stars = "⭐" * int(row['difficolta'])
        st.markdown(f"""
            <div class="language-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 24px; font-weight: bold; color: white;">{row['nome']}</span>
                    <span style="font-size: 18px;">🌍</span>
                </div>
                <div style="margin: 10px 0;">
                    <a href="https://it.wikipedia.org/wiki/Lingua_{row['nome'].replace(' ', '_')}" target="_blank" class="wiki-link">📖 Wikipedia</a>
                </div>
                <div style="color: #b0b0cc; font-size: 14px;">
                    <b>Speakers:</b> {row['speakers']}<br>
                    <b>Difficoltà:</b> {stars}
                </div>
                <div style="margin-top: 15px; text-align: right;">
                    <a href="{row['link_learn']}" target="_blank" 
                       style="text-decoration:none; background-color: #4dabff; color: white; 
                              padding: 8px 16px; border-radius: 8px; font-weight: bold; font-size: 13px;">
                       LEARN 🚀
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("Nessuna lingua trovata con i filtri correnti.")
