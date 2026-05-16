import streamlit as st
import pandas as pd

# --- CONFIG ---
st.set_page_config(page_title="OMNILINGUA", layout="wide", page_icon="🌐")

BANNER_URL = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop"

# --- STYLES ---
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=DM+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>

    * {{ box-sizing: border-box; }}
    .stApp {{ background-color: #050517; font-family: 'DM Sans', sans-serif; }}

    .block-container {{
        background-color: #0d0d2b;
        max-width: 900px !important;
        padding: 0 0 32px 0 !important;
        box-shadow: 0 0 80px rgba(0,0,0,0.6), 0 0 40px rgba(77,171,255,0.04);
        margin-top: 10px;
        border-radius: 24px;
        overflow: hidden;
    }}

    /* Banner */
    .banner {{
        width: 100%;
        height: 190px;
        background-image:
            linear-gradient(to bottom, rgba(13,13,43,0.4) 0%, rgba(13,13,43,1) 100%),
            url('{BANNER_URL}');
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 8px;
        position: relative;
    }}

    .banner::before {{
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse 60% 80% at 50% 60%, rgba(77,171,255,0.08), transparent);
    }}

    .main-title {{
        font-family: 'Orbitron', sans-serif;
        color: white;
        font-size: clamp(28px, 8vw, 56px);
        font-weight: 900;
        letter-spacing: 6px;
        text-shadow: 0 0 30px rgba(77,171,255,0.8), 0 0 60px rgba(77,171,255,0.4);
        text-align: center;
        animation: glowPulse 3s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }}

    .banner-sub {{
        font-size: 12px;
        letter-spacing: 3px;
        color: rgba(77,171,255,0.7);
        text-transform: uppercase;
        position: relative;
        z-index: 1;
    }}

    @keyframes glowPulse {{
        0%, 100% {{ text-shadow: 0 0 30px rgba(77,171,255,0.8), 0 0 60px rgba(77,171,255,0.4); }}
        50%       {{ text-shadow: 0 0 50px rgba(77,171,255,1), 0 0 100px rgba(77,171,255,0.6); }}
    }}

    .content-pad {{ padding: 24px 28px; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: #0a0a1f !important;
        border-right: 1px solid rgba(77,171,255,0.12) !important;
    }}

    [data-testid="stSidebar"] * {{
        font-family: 'DM Sans', sans-serif !important;
    }}

    [data-testid="stSidebar"] .stTextInput input {{
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(77,171,255,0.22) !important;
        border-radius: 10px !important;
        color: white !important;
        font-size: 14px !important;
    }}

    [data-testid="stSidebar"] .stTextInput input:focus {{
        border-color: #4dabff !important;
        box-shadow: 0 0 0 3px rgba(77,171,255,0.15) !important;
    }}

    [data-testid="stSidebar"] .stSelectbox > div > div {{
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(77,171,255,0.22) !important;
        border-radius: 10px !important;
        color: white !important;
    }}

    [data-testid="stSidebar"] label {{
        color: #8888aa !important;
        font-size: 11px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }}

    /* Results bar */
    .results-bar {{
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #6666aa;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(77,171,255,0.12);
    }}

    /* Card */
    .language-card {{
        background: rgba(255,255,255,0.03);
        padding: 20px;
        border-radius: 16px;
        margin-bottom: 14px;
        border: 1px solid rgba(77,171,255,0.18);
        position: relative;
        overflow: hidden;
        transition: border-color 0.25s, transform 0.25s, box-shadow 0.25s;
        animation: cardIn 0.35s ease both;
    }}

    .language-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(to right, transparent, #4dabff, transparent);
        opacity: 0;
        transition: opacity 0.3s;
    }}

    .language-card:hover {{
        border-color: rgba(77,171,255,0.5);
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(77,171,255,0.1);
    }}
    .language-card:hover::before {{ opacity: 1; }}

    @keyframes cardIn {{
        from {{ opacity: 0; transform: translateY(14px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}

    .card-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }}

    .lang-name {{ font-size: 20px; font-weight: 700; color: white; }}

    .card-meta {{
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
        color: #8888aa;
        font-size: 13px;
        margin-bottom: 14px;
    }}
    .card-meta b {{ color: #c8c8e0; }}

    .card-actions {{
        display: flex;
        gap: 10px;
        justify-content: flex-end;
        flex-wrap: wrap;
    }}

    .btn-wiki {{
        display: inline-flex; align-items: center; gap: 5px;
        color: #4dabff; font-size: 12px; font-weight: 600;
        text-decoration: none; padding: 7px 14px;
        border-radius: 8px; border: 1px solid rgba(77,171,255,0.25);
        background: transparent; transition: background 0.2s, border-color 0.2s;
    }}
    .btn-wiki:hover {{
        background: rgba(77,171,255,0.12);
        border-color: #4dabff;
        color: #4dabff;
    }}

    .btn-learn {{
        display: inline-flex; align-items: center; gap: 6px;
        background: #4dabff; color: #050517;
        font-size: 12px; font-weight: 800; letter-spacing: 1.5px;
        text-transform: uppercase; text-decoration: none;
        padding: 8px 18px; border-radius: 8px;
        transition: box-shadow 0.2s, transform 0.15s;
    }}
    .btn-learn:hover {{
        box-shadow: 0 0 20px rgba(77,171,255,0.6);
        transform: translateY(-1px);
        color: #050517;
    }}

    /* Stat box sidebar */
    .stat-box {{
        background: rgba(77,171,255,0.08);
        border: 1px solid rgba(77,171,255,0.2);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-top: 8px;
    }}
    .stat-num {{ font-size: 32px; font-weight: 700; color: #4dabff; display: block; }}
    .stat-label {{ font-size: 11px; color: #6666aa; letter-spacing: 2px; text-transform: uppercase; }}

    .empty-state {{ text-align: center; padding: 60px 20px; color: #6666aa; }}
    .empty-icon {{ font-size: 48px; display: block; margin-bottom: 12px; opacity: 0.5; }}

    #MainMenu, footer, header {{ visibility: hidden; }}
    .stDeployButton {{ display: none; }}
    </style>

    <div class="banner">
        <div class="main-title">OMNILINGUA</div>
        <div class="banner-sub">Esplora le lingue del mondo</div>
    </div>
""", unsafe_allow_html=True)


# --- LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_csv('lingue.csv')

df = load_data()


# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🔍 Filtri")
    st.markdown("---")

    search = st.text_input("Cerca lingua", placeholder="Es. Giapponese…")

    st.markdown("<br>", unsafe_allow_html=True)

    diff_options = ["Tutte", "⭐ (1)", "⭐⭐ (2)", "⭐⭐⭐ (3)", "⭐⭐⭐⭐ (4)", "⭐⭐⭐⭐⭐ (5)"]
    diff_filter = st.selectbox("Difficoltà (esatta)", diff_options)

    st.markdown("<br>", unsafe_allow_html=True)

    sort_by = st.selectbox("Ordina per", ["Nome", "Parlanti", "Difficoltà"])
    sort_dir = st.selectbox("Ordine", ["↑ Crescente", "↓ Decrescente"])


# --- FILTER ---
ascending = sort_dir == "↑ Crescente"

filtered_df = df[df['nome'].str.contains(search, case=False, na=False)].copy()

# Difficoltà esatta
if diff_filter != "Tutte":
    exact_diff = diff_options.index(diff_filter)  # indice 1-5 corrisponde alla difficoltà
    filtered_df = filtered_df[filtered_df['difficolta'] == exact_diff]

# --- SORT ---
if sort_by == "Nome":
    filtered_df = filtered_df.sort_values('nome', ascending=ascending)
elif sort_by == "Difficoltà":
    filtered_df = filtered_df.sort_values('difficolta', ascending=ascending)
elif sort_by == "Parlanti":
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

    filtered_df['_spk_num'] = filtered_df['speakers'].apply(parse_speakers)
    filtered_df = filtered_df.sort_values('_spk_num', ascending=ascending)
    filtered_df = filtered_df.drop(columns=['_spk_num'])

# Stat box
with st.sidebar:
    count = len(filtered_df)
    st.markdown(f"""
        <div class="stat-box">
            <span class="stat-num">{count}</span>
            <span class="stat-label">Lingue trovate</span>
        </div>
    """, unsafe_allow_html=True)


# --- CARDS ---
st.markdown('<div class="content-pad">', unsafe_allow_html=True)

label = f"{count} lingua{'e' if count != 1 else ''} trovata{'e' if count != 1 else ''}"
st.markdown(f'<div class="results-bar">{label}</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    for i, (_, row) in enumerate(filtered_df.iterrows()):
        stars = "⭐" * int(row['difficolta'])
        wiki_url = f"https://it.wikipedia.org/wiki/Lingua_{row['nome'].replace(' ', '_')}"
        delay = i * 0.05

        st.markdown(f"""
            <div class="language-card" style="animation-delay:{delay}s">
                <div class="card-header">
                    <span class="lang-name">{row['nome']}</span>
                    <span style="font-size:22px; opacity:0.6;">🌍</span>
                </div>
                <div class="card-meta">
                    <div>Parlanti: <b>{row['speakers']}</b></div>
                    <div>Difficoltà: <b>{stars}</b></div>
                </div>
                <div class="card-actions">
                    <a href="{wiki_url}" target="_blank" class="btn-wiki">📖 Wikipedia</a>
                    <a href="{row['link_learn']}" target="_blank" class="btn-learn">LEARN 🚀</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="empty-state">
            <span class="empty-icon">🌐</span>
            Nessuna lingua corrisponde ai filtri.
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
