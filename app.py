import os
import base64
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go

# ==============================================================================
# KONFIGURASI LOGO & FAVICON (OTOMATIS MEMBACA pertamina2.png)
# ==============================================================================
LOGO_FILE = "pertamina2.png"
HAS_LOGO = os.path.exists(LOGO_FILE)

def get_logo_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==============================================================================
# KONFIGURASI HALAMAN & FAVICON
# ==============================================================================
st.set_page_config(
    page_title="ARMAKUNG Maritime Command Center 2026",
    page_icon=LOGO_FILE if HAS_LOGO else "🚢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# CUSTOM CSS: DARK COMMAND CENTER + FIX HEADER + ANIMASI CAHAYA + RESPONSIVE
# ==============================================================================
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at 50% 0%, #102a4e 0%, #050d1a 68%);
        color: #e2e8f0;
        -webkit-tap-highlight-color: transparent;
    }
    header[data-testid="stHeader"] {
        background: rgba(5, 13, 26, 0.72);
        backdrop-filter: blur(6px);
    }
    .block-container {
        padding-top: 3.6rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        max-width: 100%;
    }

    @keyframes scanLine {
        0%   { left: -35%; opacity: 0; }
        15%  { opacity: 1; }
        85%  { opacity: 1; }
        100% { left: 105%; opacity: 0; }
    }
    @keyframes neonPulse {
        0%, 100% { text-shadow: 0 0 12px rgba(0, 229, 255, 0.55), 0 0 24px rgba(0, 229, 255, 0.25); }
        50%      { text-shadow: 0 0 20px rgba(0, 229, 255, 0.95), 0 0 38px rgba(56, 189, 248, 0.45); }
    }
    @keyframes amberGlow {
        0%, 100% { text-shadow: 0 0 10px rgba(255, 123, 58, 0.45); }
        50%      { text-shadow: 0 0 18px rgba(255, 123, 58, 0.85), 0 0 28px rgba(255, 123, 58, 0.35); }
    }
    @keyframes borderBreath {
        0%, 100% { box-shadow: inset 0 0 14px rgba(0, 229, 255, 0.10), 0 0 10px rgba(0, 229, 255, 0.14); }
        50%      { box-shadow: inset 0 0 20px rgba(0, 229, 255, 0.20), 0 0 18px rgba(0, 229, 255, 0.30); }
    }

    .cmd-title-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        flex-wrap: wrap;
        text-align: center;
        padding: 0.5rem 0.5rem 0.9rem 0.5rem;
        border-bottom: 1.5px solid rgba(0, 229, 255, 0.35);
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }
    .cmd-title-wrap::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: -35%;
        width: 35%;
        height: 2.5px;
        background: linear-gradient(90deg, transparent, #00e5ff, #ffffff, #00e5ff, transparent);
        box-shadow: 0 0 12px #00e5ff;
        animation: scanLine 4.2s ease-in-out infinite;
    }
    .cmd-logo-box {
        background: rgba(255, 255, 255, 0.94);
        padding: 6px 12px;
        border-radius: 8px;
        border: 1.5px solid rgba(0, 229, 255, 0.75);
        box-shadow: 0 0 14px rgba(0, 229, 255, 0.35);
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .cmd-logo-box:hover {
        transform: scale(1.04);
        box-shadow: 0 0 22px rgba(0, 229, 255, 0.65);
    }
    .cmd-logo-box img {
        height: clamp(32px, 3.6vw, 46px);
        width: auto;
        object-fit: contain;
        display: block;
    }
    .cmd-title {
        font-family: 'Segoe UI', sans-serif;
        font-size: clamp(1.1rem, 2.05vw, 1.9rem);
        font-weight: 800;
        letter-spacing: 1.6px;
        color: #38e8ff;
        animation: neonPulse 3.5s ease-in-out infinite;
        margin: 0;
        line-height: 1.25;
    }
    .cmd-subtitle {
        font-size: clamp(0.66rem, 0.95vw, 0.82rem);
        color: #94a3b8;
        letter-spacing: 0.9px;
        margin-top: 4px;
    }

    .kpi-box {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(13, 35, 66, 0.88), rgba(7, 20, 40, 0.94));
        border: 1px solid rgba(0, 229, 255, 0.50);
        border-radius: 7px;
        padding: 0.8rem 1.05rem;
        margin-bottom: 0.7rem;
        cursor: pointer;
        animation: borderBreath 4.5s ease-in-out infinite;
        transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1),
                    border-color 0.28s ease,
                    box-shadow 0.28s ease;
    }
    .kpi-box::before {
        content: "";
        position: absolute;
        top: 0;
        left: -120%;
        width: 75%;
        height: 100%;
        background: linear-gradient(115deg, transparent 20%, rgba(0, 229, 255, 0.22) 50%, transparent 80%);
        transition: left 0.6s ease;
        pointer-events: none;
    }
    .kpi-box:hover, .kpi-box:active {
        transform: translateY(-4px) scale(1.015);
        border-color: #00e5ff;
        box-shadow: inset 0 0 22px rgba(0, 229, 255, 0.24), 0 8px 24px rgba(0, 229, 255, 0.35);
    }
    .kpi-box:hover::before, .kpi-box:active::before {
        left: 140%;
    }
    .kpi-label {
        font-size: clamp(0.72rem, 0.9vw, 0.85rem);
        font-weight: 600;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .kpi-value-row {
        display: flex;
        flex-wrap: wrap;
        align-items: baseline;
        justify-content: space-between;
        gap: 6px;
        margin-top: 4px;
    }
    .kpi-val {
        font-size: clamp(1.35rem, 1.9vw, 1.8rem);
        font-weight: 800;
        color: #ff7b3a;
        animation: amberGlow 3s ease-in-out infinite;
    }
    .kpi-unit {
        font-size: clamp(0.72rem, 0.85vw, 0.82rem);
        color: #7dd3fc;
        font-weight: 600;
    }

    .info-card {
        position: relative;
        overflow: hidden;
        background: rgba(8, 22, 44, 0.78);
        border: 1px solid rgba(0, 229, 255, 0.32);
        border-radius: 7px;
        padding: 11px;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .info-card:hover, .info-card:active {
        transform: translateY(-3px);
        border-color: #00e5ff;
        box-shadow: 0 6px 20px rgba(0, 229, 255, 0.28);
    }
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 6px 4px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 4px;
        transition: background 0.2s ease, padding-left 0.2s ease;
    }
    .info-row:hover, .info-row:active {
        background: rgba(0, 229, 255, 0.10);
        padding-left: 8px;
    }
    .info-row:last-child { border-bottom: none; }

    .panel-header {
        background: linear-gradient(90deg, rgba(0, 229, 255, 0.20), transparent);
        border-left: 3px solid #00e5ff;
        padding: 5px 10px;
        font-size: clamp(0.82rem, 1vw, 0.94rem);
        font-weight: 700;
        color: #67e8f9;
        letter-spacing: 0.4px;
        margin-bottom: 6px;
        margin-top: 4px;
        transition: border-left-width 0.2s ease, background 0.25s ease, color 0.2s ease;
    }
    .panel-header:hover {
        border-left-width: 6px;
        background: linear-gradient(90deg, rgba(0, 229, 255, 0.34), transparent);
        color: #ffffff;
    }

    div[data-testid="stPlotlyChart"] {
        border: 1px solid rgba(0, 229, 255, 0.22);
        border-radius: 7px;
        overflow: hidden;
        transition: border-color 0.28s ease, box-shadow 0.28s ease, transform 0.25s ease;
    }
    div[data-testid="stPlotlyChart"]:hover {
        border-color: rgba(0, 229, 255, 0.78);
        box-shadow: 0 0 18px rgba(0, 229, 255, 0.26);
        transform: translateY(-2px);
    }

    .stButton > button, .stDownloadButton > button {
        border: 1px solid rgba(0, 229, 255, 0.55) !important;
        transition: transform 0.18s ease, box-shadow 0.25s ease !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        box-shadow: 0 0 14px rgba(0, 229, 255, 0.45) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active, .stDownloadButton > button:active {
        transform: scale(0.97) !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #071326;
        border-right: 1px solid rgba(0, 229, 255, 0.3);
    }

    @media (max-width: 768px) {
        .block-container {
            padding-top: 3.2rem !important;
            padding-left: 0.65rem !important;
            padding-right: 0.65rem !important;
        }
        .kpi-box { padding: 0.65rem 0.8rem; }
        .cmd-title-wrap { gap: 10px; }
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA AKTUAL 2026 (JANUARI – OKTOBER 2026, 19 CALL)
# ==============================================================================
MONTH_ORDER = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Mei": 5, "Jun": 6,
    "Jul": 7, "Agt": 8, "Sep": 9, "Okt": 10, "Nov": 11, "Des": 12
}
MONTH_LIST = list(MONTH_ORDER.keys())
VESSEL_LIST = ["TB. AQUA HARBOUR", "TB. MEDELIN CITRA", "TB. MEDELIN PARTNER"]

INITIAL_DATA = [
    {"Bulan": "Jan", "Kapal": "TB. AQUA HARBOUR", "Delivery": "31/01/2026", "Redelivery": "03/02/2026", "Durasi": 3.43, "HSD_L": 8307, "Harga_HSD": 19375, "Sewa": 168233333, "HSD_Rp": 160948125, "PBBKB": 15513323},
    {"Bulan": "Feb", "Kapal": "TB. MEDELIN CITRA", "Delivery": "15/02/2026", "Redelivery": "18/02/2026", "Durasi": 2.98, "HSD_L": 8424, "Harga_HSD": 19375, "Sewa": 146183333, "HSD_Rp": 163215000, "PBBKB": 15731820},
    {"Bulan": "Feb", "Kapal": "TB. AQUA HARBOUR", "Delivery": "24/02/2026", "Redelivery": "27/02/2026", "Durasi": 3.38, "HSD_L": 7978, "Harga_HSD": 19555, "Sewa": 165375000, "HSD_Rp": 156009790, "PBBKB": 15042519},
    {"Bulan": "Mar", "Kapal": "TB. MEDELIN CITRA", "Delivery": "08/03/2026", "Redelivery": "11/03/2026", "Durasi": 2.72, "HSD_L": 8107, "Harga_HSD": 19555, "Sewa": 133320833, "HSD_Rp": 158532385, "PBBKB": 15285749},
    {"Bulan": "Mar", "Kapal": "TB. AQUA HARBOUR", "Delivery": "14/03/2026", "Redelivery": "17/03/2026", "Durasi": 3.35, "HSD_L": 8452, "Harga_HSD": 19555, "Sewa": 164354167, "HSD_Rp": 165278860, "PBBKB": 15936246},
    {"Bulan": "Apr", "Kapal": "TB. MEDELIN CITRA", "Delivery": "04/04/2026", "Redelivery": "07/04/2026", "Durasi": 2.55, "HSD_L": 8363, "Harga_HSD": 19825, "Sewa": 125052083, "HSD_Rp": 165796475, "PBBKB": 15994238},
    {"Bulan": "Apr", "Kapal": "TB. AQUA HARBOUR", "Delivery": "09/04/2026", "Redelivery": "12/04/2026", "Durasi": 3.15, "HSD_L": 8031, "Harga_HSD": 19825, "Sewa": 154554167, "HSD_Rp": 159214575, "PBBKB": 15359288},
    {"Bulan": "Mei", "Kapal": "TB. AQUA HARBOUR", "Delivery": "03/05/2026", "Redelivery": "06/05/2026", "Durasi": 3.32, "HSD_L": 8039, "Harga_HSD": 28195, "Sewa": 162720833, "HSD_Rp": 226659605, "PBBKB": 22103231},
    {"Bulan": "Mei", "Kapal": "TB. MEDELIN CITRA", "Delivery": "29/05/2026", "Redelivery": "01/06/2026", "Durasi": 3.35, "HSD_L": 8700, "Harga_HSD": 24415, "Sewa": 164150000, "HSD_Rp": 212410500, "PBBKB": 20632050},
    {"Bulan": "Jun", "Kapal": "TB. MEDELIN CITRA", "Delivery": "22/06/2026", "Redelivery": "24/06/2026", "Durasi": 1.29, "HSD_L": 7144, "Harga_HSD": 24415, "Sewa": 63291667, "HSD_Rp": 174420760, "PBBKB": 16941996},
    {"Bulan": "Jul", "Kapal": "TB. AQUA HARBOUR", "Delivery": "04/07/2026", "Redelivery": "07/07/2026", "Durasi": 2.73, "HSD_L": 7914, "Harga_HSD": 23245, "Sewa": 133933333, "HSD_Rp": 183960930, "PBBKB": 17842113},
    {"Bulan": "Jul", "Kapal": "TB. MEDELIN PARTNER", "Delivery": "08/07/2026", "Redelivery": "09/07/2026", "Durasi": 1.41, "HSD_L": 3660, "Harga_HSD": 23245, "Sewa": 69008333, "HSD_Rp": 85076700, "PBBKB": 8251470},
    {"Bulan": "Jul", "Kapal": "TB. MEDELIN PARTNER", "Delivery": "19/07/2026", "Redelivery": "21/07/2026", "Durasi": 1.66, "HSD_L": 3999, "Harga_HSD": 23245, "Sewa": 81258333, "HSD_Rp": 92956755, "PBBKB": 9015746},
    {"Bulan": "Agt", "Kapal": "TB. AQUA HARBOUR", "Delivery": "10/08/2026", "Redelivery": "13/08/2026", "Durasi": 2.14, "HSD_L": 7062, "Harga_HSD": 17080, "Sewa": 104737500, "HSD_Rp": 120618960, "PBBKB": 11567556},
    {"Bulan": "Agt", "Kapal": "TB. MEDELIN CITRA", "Delivery": "24/08/2026", "Redelivery": "26/08/2026", "Durasi": 1.59, "HSD_L": 7708, "Harga_HSD": 17080, "Sewa": 77991667, "HSD_Rp": 131652640, "PBBKB": 12625704},
    {"Bulan": "Sep", "Kapal": "TB. MEDELIN PARTNER", "Delivery": "08/09/2026", "Redelivery": "10/09/2026", "Durasi": 1.65, "HSD_L": 4238, "Harga_HSD": 17080, "Sewa": 80645833, "HSD_Rp": 72385040, "PBBKB": 6941844},
    {"Bulan": "Sep", "Kapal": "TB. AQUA HARBOUR", "Delivery": "20/09/2026", "Redelivery": "23/09/2026", "Durasi": 3.11, "HSD_L": 7381, "Harga_HSD": 17755, "Sewa": 152512500, "HSD_Rp": 131049655, "PBBKB": 12588296},
    {"Bulan": "Sep", "Kapal": "TB. MEDELIN PARTNER", "Delivery": "29/09/2026", "Redelivery": "01/10/2026", "Durasi": 1.65, "HSD_L": 4205, "Harga_HSD": 17755, "Sewa": 81054167, "HSD_Rp": 74659775, "PBBKB": 7171628},
    {"Bulan": "Okt", "Kapal": "TB. MEDELIN PARTNER", "Delivery": "23/10/2026", "Redelivery": "25/10/2026", "Durasi": 1.60, "HSD_L": 4050, "Harga_HSD": 17755, "Sewa": 78604167, "HSD_Rp": 71907750, "PBBKB": 6907275},
]

if "df_data" not in st.session_state:
    st.session_state.df_data = pd.DataFrame(INITIAL_DATA)

# ==============================================================================
# SIDEBAR: FILTER & UPLOAD CSV
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Filter & Pengaturan")
    basis_pajak = st.radio(
        "Basis Perhitungan:",
        ["Tanpa Pajak (Sewa + HSD)", "Grand Total (Incl. PBBKB 10%)"],
        index=0
    )
    include_tax = basis_pajak == "Grand Total (Incl. PBBKB 10%)"

    df_src = st.session_state.df_data.copy()
    all_vessels = sorted(df_src["Kapal"].dropna().unique().tolist())
    sel_vessels = st.multiselect("Armada Tugboat:", all_vessels, default=all_vessels)
    sel_cats = st.multiselect("Kategori Layanan:", ["Full Service", "Berthing Only"], default=["Full Service", "Berthing Only"])

    st.divider()
    st.markdown("### 📂 Muat Data dari CSV")
    uploaded_csv = st.file_uploader("Upload CSV hasil ekspor sebelumnya:", type=["csv"])
    if uploaded_csv is not None:
        try:
            df_up = pd.read_csv(uploaded_csv)
            req_cols = ["Bulan", "Kapal", "Delivery", "Redelivery", "Durasi", "HSD_L", "Harga_HSD", "Sewa", "HSD_Rp", "PBBKB"]
            if all(c in df_up.columns for c in req_cols):
                st.session_state.df_data = df_up[req_cols].copy()
                st.success("Data CSV berhasil dimuat!")
                st.rerun()
            else:
                st.error("Kolom CSV tidak sesuai format ARMAKUNG.")
        except Exception as e:
            st.error(f"Gagal membaca CSV: {e}")

    if st.button("🔄 Reset ke 19 Call Aktual", use_container_width=True):
        st.session_state.df_data = pd.DataFrame(INITIAL_DATA)
        st.rerun()

# ==============================================================================
# PROSES & KALKULASI DATA
# ==============================================================================
df_all = st.session_state.df_data.copy()
for col in ["Durasi", "HSD_L", "Harga_HSD", "Sewa", "HSD_Rp", "PBBKB"]:
    df_all[col] = pd.to_numeric(df_all[col], errors="coerce").fillna(0)

df_all["Urutan"] = df_all["Bulan"].map(MONTH_ORDER).fillna(12).astype(int)
df_all["Tanpa_Pajak"] = df_all["Sewa"] + df_all["HSD_Rp"]
df_all["Grand_Total"] = df_all["Tanpa_Pajak"] + df_all["PBBKB"]
df_all["Kategori"] = df_all["Durasi"].apply(lambda x: "Full Service" if x > 2.0 else "Berthing Only")

df = df_all[(df_all["Kapal"].isin(sel_vessels)) & (df_all["Kategori"].isin(sel_cats))].copy()
rev_col = "Grand_Total" if include_tax else "Tanpa_Pajak"
active_months = max(10, int(df_all["Urutan"].max())) if len(df_all) > 0 else 10
prorata = 12 / active_months

total_rev = df[rev_col].sum()
proj_rev = total_rev * prorata
total_calls = len(df)
ann_calls = total_calls * prorata
full_df = df[df["Durasi"] > 2.0]
potensi_rev = (full_df[rev_col].mean() * ann_calls) if len(full_df) > 0 else proj_rev

# ==============================================================================
# HEADER COMMAND CENTER DENGAN LOGO pertamina2.png
# ==============================================================================
logo_html = ""
if HAS_LOGO:
    b64_logo = get_logo_base64(LOGO_FILE)
    logo_html = f'<div class="cmd-logo-box"><img src="data:image/png;base64,{b64_logo}" alt="Logo Perusahaan"></div>'

st.markdown(f"""
<div class="cmd-title-wrap">
    {logo_html}
    <div>
        <div class="cmd-title">ARMAKUNG MARITIME MONITORING &amp; FUEL COMMAND CENTER</div>
        <div class="cmd-subtitle">PT NUSANTARA REGAS </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# BARIS 1: 3 KARTU KPI UTAMA
# ==============================================================================
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"""
    <div class="kpi-box" tabindex="0">
        <div class="kpi-label">Realisasi Revenue YTD ({active_months} Bulan)</div>
        <div class="kpi-value-row">
            <span class="kpi-val">{total_rev/1e9:,.2f} Miliar</span>
            <span class="kpi-unit">IDR &bull; {total_calls} Call Aktual</span>
        </div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-box" tabindex="0">
        <div class="kpi-label">Proyeksi 1 Tahun Anggaran (12/{active_months})</div>
        <div class="kpi-value-row">
            <span class="kpi-val">{proj_rev/1e9:,.2f} Miliar</span>
            <span class="kpi-unit">IDR &bull; {ann_calls:.1f} Call/Thn</span>
        </div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-box" tabindex="0">
        <div class="kpi-label">Potensi Full Service 2026</div>
        <div class="kpi-value-row">
            <span class="kpi-val">{potensi_rev/1e9:,.2f} Miliar</span>
            <span class="kpi-unit">IDR &bull; Zero CAPEX</span>
        </div>
    </div>""", unsafe_allow_html=True)

PLOT_BG = "rgba(8, 22, 44, 0.72)"
FONT_CLR = "#cbd5e1"
GRID_CLR = "rgba(0, 229, 255, 0.14)"

# ==============================================================================
# BARIS 2: ARMADA | PETA MARITIM (100% BEBAS API KEY) | KOMPOSISI & REKOR
# ==============================================================================
col_left, col_mid, col_right = st.columns([1.15, 2.35, 1.15], gap="small")

with col_left:
    st.markdown('<div class="panel-header">⚓ Revenue per Armada (Miliar Rp)</div>', unsafe_allow_html=True)
    v_agg = df.groupby("Kapal", as_index=False).agg(Rev=(rev_col, "sum"), Calls=("Bulan", "count")).sort_values("Rev")
    max_v = (v_agg["Rev"].max() / 1e9) * 1.28 if len(v_agg) > 0 else 3
    fig_hbar = go.Figure(go.Bar(
        x=v_agg["Rev"] / 1e9,
        y=v_agg["Kapal"].str.replace("TB. ", ""),
        orientation="h",
        marker=dict(color=["#38bdf8", "#6366f1", "#00e5ff"][:len(v_agg)], line=dict(color="#00e5ff", width=1)),
        text=[f"Rp {r/1e9:.2f}M ({c}x)" for r, c in zip(v_agg["Rev"], v_agg["Calls"])],
        textposition="auto",
        textfont=dict(size=10, family="Segoe UI"),
        hovertemplate="<b>%{y}</b><br>Revenue: Rp %{x:.2f} M<extra></extra>"
    ))
    fig_hbar.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_CLR, size=10),
        height=245, margin=dict(l=8, r=18, t=12, b=30),
        xaxis=dict(gridcolor=GRID_CLR, title="Miliar Rp", range=[0, max_v], automargin=True),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", automargin=True)
    )
    st.plotly_chart(fig_hbar, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="panel-header">⏱️ Ringkasan Operasional YTD</div>', unsafe_allow_html=True)
    total_jam = df["Durasi"].sum() * 24
    total_hsd = df["HSD_L"].sum()
    st.markdown(f"""
    <div class="info-card" style="font-size:0.84rem;" tabindex="0">
        <div class="info-row">
            <span style="color:#94a3b8;">Total Durasi</span>
            <b style="color:#00e5ff;">{df['Durasi'].sum():.2f} Hr ({total_jam:,.0f} Jam)</b>
        </div>
        <div class="info-row">
            <span style="color:#94a3b8;">Total HSD</span>
            <b style="color:#ffeb3b;">{total_hsd:,.0f} Liter</b>
        </div>
        <div class="info-row">
            <span style="color:#94a3b8;">Layanan</span>
            <b style="color:#4ade80;">{len(full_df)} Full / {len(df)-len(full_df)} Partial</b>
        </div>
        <div class="info-row">
            <span style="color:#94a3b8;">Lead Time</span>
            <b style="color:#ff7b3a;">52,13 Jam (748% Cepat)</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_mid:
    st.markdown('<div class="panel-header">🗺️ Live Maritime Route &amp; Fuel Calculator (NR OptiVoyage)</div>', unsafe_allow_html=True)

    map_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css"/>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css"/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>
        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>
        <style>
            * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
            html, body { width:100%; height:100%; margin:0; padding:0; background:#050d1a; font-family:'Segoe UI',sans-serif; overflow:hidden; }
            .wrap { position:relative; width:100%; height:100%; display:flex; flex-direction:column; border:1px solid rgba(0,229,255,0.40); border-radius:7px; overflow:hidden; }
            #map { flex:1; width:100%; min-height:240px; background:#050d1a; }

            /* Filter Deep Navy untuk OpenStreetMap (100% Tanpa API Key) */
            .dark-navy-tiles {
                filter: invert(100%) hue-rotate(190deg) brightness(86%) contrast(95%) saturate(135%);
            }

            @keyframes routeFlow {
                from { stroke-dashoffset: 44; }
                to   { stroke-dashoffset: 0; }
            }
            path.route-glow { filter: drop-shadow(0 0 8px #00e5ff); }
            path.route-pulse {
                stroke-dasharray: 12, 10;
                animation: routeFlow 1.1s linear infinite;
                filter: drop-shadow(0 0 6px #ffffff);
            }

            .leaflet-control-layers {
                background: rgba(10, 22, 42, 0.92) !important;
                color: #e2e8f0 !important;
                border: 1px solid rgba(0, 229, 255, 0.6) !important;
                border-radius: 6px !important;
                font-size: 10.5px !important;
            }
            .leaflet-control-layers-separator { border-top-color: rgba(0, 229, 255, 0.3) !important; }

            .calc-panel {
                position: absolute; top: 8px; right: 8px; width: 255px;
                background: rgba(10, 22, 42, 0.94); color: #fff; z-index: 9999;
                border: 1px solid rgba(0, 229, 255, 0.75); border-radius: 7px;
                box-shadow: 0 0 16px rgba(0, 229, 255, 0.28); backdrop-filter: blur(6px);
                overflow: hidden;
                transition: box-shadow 0.25s ease, border-color 0.25s ease;
            }
            .calc-panel:hover {
                border-color: #00e5ff;
                box-shadow: 0 0 24px rgba(0, 229, 255, 0.45);
            }
            .calc-hdr {
                background: linear-gradient(90deg, #0b2545, #133c6e); padding: 6px 9px;
                display:flex; justify-content:space-between; align-items:center;
                border-bottom: 1.5px solid #00e5ff; cursor: pointer;
                transition: background 0.2s ease;
            }
            .calc-hdr:hover { background: linear-gradient(90deg, #103460, #1a4f8f); }
            .calc-body { padding: 8px; font-size: 10.5px; }
            .cfg-box { background: rgba(0,229,255,0.08); border:1px solid rgba(0,229,255,0.35); border-radius:4px; padding:6px; margin-bottom:6px; }
            .row2 { display:flex; justify-content:space-between; gap:5px; margin-top:3px; }
            input, select {
                background:#061124; color:#fff; border:1px solid #334155; border-radius:3px;
                padding:2px 4px; font-size:10.5px; width:100%;
                transition: border-color 0.2s ease, box-shadow 0.2s ease;
            }
            input:focus, select:focus {
                outline: none; border-color: #00e5ff; box-shadow: 0 0 8px rgba(0,229,255,0.5);
            }
            .wx-box { background: rgba(0,0,0,0.35); border:1px solid #334155; border-radius:4px; padding:5px; margin-bottom:6px; }
            .wx-grid { display:flex; justify-content:space-between; text-align:center; margin-top:2px; }
            .btn-sm {
                border:none; border-radius:3px; padding:4px 5px; font-size:9.5px; font-weight:700; cursor:pointer;
                transition: transform 0.15s ease, filter 0.2s ease;
            }
            .btn-sm:hover { filter: brightness(1.15); transform: translateY(-1px); }
            .btn-sm:active { transform: scale(0.94); }
            table { width:100%; border-collapse:collapse; margin-top:5px; font-size:10.5px; }
            td { padding:3px 2px; border-bottom:1px solid rgba(255,255,255,0.09); }
            tr:hover td { background: rgba(0,229,255,0.08); }
            .val { text-align:right; font-weight:700; }

            @media (max-width: 600px) {
                html, body { overflow-y: auto; }
                .wrap { height: auto; }
                #map { height: 240px; flex: none; }
                .calc-panel { position: relative; top: 0; right: 0; width: 100%; margin-top: 6px; border-radius: 6px; }
            }
        </style>
    </head>
    <body>
        <div class="wrap">
            <div id="map"></div>
            <div class="calc-panel">
                <div class="calc-hdr" onclick="toggleCalc()">
                    <span style="color:#00e5ff; font-weight:800; font-size:11px;">⛽ NR FUEL &amp; CHARTER CALC</span>
                    <span id="btn_tog" style="color:#fff; font-weight:bold;">−</span>
                </div>
                <div id="calc_body" class="calc-body">
                    <div class="cfg-box">
                        <div class="row2">
                            <div style="flex:1;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <label style="font-size:9px; color:#94a3b8;">Fuel</label>
                                    <select id="sel_unit" onchange="updateCalc()" style="width:auto; font-size:8.5px; padding:0 2px; color:#00e5ff;">
                                        <option value="lnm">L/NM</option>
                                        <option value="lhr">L/Hr</option>
                                    </select>
                                </div>
                                <input type="number" id="inp_faktor" value="51.07" step="0.1" oninput="updateCalc()">
                            </div>
                            <div style="flex:1;">
                                <label style="font-size:9px; color:#94a3b8;">Speed (kn)</label>
                                <input type="number" id="inp_speed" value="10.0" step="0.5" oninput="updateCalc()">
                            </div>
                        </div>
                        <div class="row2">
                            <div style="flex:1;">
                                <label style="font-size:9px; color:#94a3b8;">HSD (Rp/L)</label>
                                <input type="number" id="inp_harga" value="17755" step="100" oninput="updateCalc()">
                            </div>
                            <div style="flex:1;">
                                <label style="font-size:9px; color:#94a3b8;">STS (Jam)</label>
                                <input type="number" id="inp_sts" value="24" step="2" oninput="updateCalc()">
                            </div>
                        </div>
                    </div>

                    <div class="wx-box">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="color:#00e5ff; font-size:9.5px; font-weight:700;">☁️ LIVE WEATHER</span>
                            <span id="live_status" style="font-size:8.5px; color:#94a3b8;">● Sync...</span>
                        </div>
                        <div class="wx-grid">
                            <div><span style="color:#94a3b8;font-size:8.5px;">Wind:</span> <b id="val_wind">--</b></div>
                            <div><span style="color:#94a3b8;font-size:8.5px;">Wave:</span> <b id="val_wave">--</b></div>
                            <div><span style="color:#94a3b8;font-size:8.5px;">Imp:</span> <b id="val_impact" style="color:#ffeb3b;">--</b></div>
                        </div>
                    </div>

                    <div class="row2" style="margin-bottom:5px;">
                        <div style="flex:1;">
                            <select id="sel_start" onchange="changeRoute()">
                                <option value="nr" selected>From: FSRU NR 1</option>
                                <option value="lampung">From: FSRU Lampung</option>
                                <option value="jsp">From: Jawa Satu</option>
                                <option value="priok">From: Priok</option>
                            </select>
                        </div>
                        <div style="flex:1;">
                            <select id="sel_end" onchange="changeRoute()">
                                <option value="lampung" selected>To: FSRU Lampung</option>
                                <option value="jsp">To: Jawa Satu</option>
                                <option value="priok">To: Priok</option>
                                <option value="nr">To: FSRU NR 1</option>
                            </select>
                        </div>
                    </div>

                    <div class="row2" style="margin-bottom:3px;">
                        <button class="btn-sm" onclick="performUndo()" style="flex:1; background:#facc15; color:#000;">↩ UNDO</button>
                        <button class="btn-sm" onclick="performRedo()" style="flex:1; background:#22c55e; color:#fff;">REDO ↪</button>
                        <button class="btn-sm" onclick="changeRoute()" style="flex:1; background:#ef4444; color:#fff;">RESET</button>
                    </div>

                    <table>
                        <tr><td style="color:#94a3b8;">Jarak OW / PP</td><td id="val_dist" class="val">--</td></tr>
                        <tr><td style="color:#94a3b8;">Speed / Durasi PP</td><td id="val_dur" class="val" style="color:#00e5ff;">--</td></tr>
                        <tr><td style="color:#94a3b8;">Est. Total BBM</td><td id="val_bbm" class="val" style="color:#ffeb3b;">--</td></tr>
                        <tr><td style="color:#94a3b8;">Biaya HSD</td><td id="val_cost_bbm" class="val">--</td></tr>
                        <tr><td style="color:#94a3b8;">Sewa (49 Jt/hr)</td><td id="val_cost_sewa" class="val">--</td></tr>
                        <tr style="background:rgba(0,229,255,0.14);">
                            <td style="color:#00e5ff; font-weight:800;">EST. TOTAL</td>
                            <td id="val_total" class="val" style="color:#ff7b3a; font-size:11.5px;">--</td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>

        <script>
            var map = L.map('map', { center: [-5.75, 106.45], zoom: 8, doubleClickZoom: false });

            // 1. Deep Navy Maritime (OpenStreetMap + Dark Navy CSS Filter — Tanpa API Key)
            var osmDark = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap', maxZoom: 19, className: 'dark-navy-tiles'
            }).addTo(map);

            // 2. Satellite Hybrid (Esri Imagery + Label Wilayah — Tanpa API Key)
            var esriSat = L.layerGroup([
                L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                    attribution: 'Esri Satellite', maxZoom: 19
                }),
                L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
                    maxZoom: 19
                })
            ]);

            // 3. Ocean Bathymetry (Esri Ocean Base + Label Laut — Tanpa API Key)
            var esriOcean = L.layerGroup([
                L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}', {
                    attribution: 'Esri Ocean', maxZoom: 13
                }),
                L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Reference/MapServer/tile/{z}/{y}/{x}', {
                    maxZoom: 13
                })
            ]);

            // 4. Street Map Light (OpenStreetMap Standar — Tanpa API Key)
            var osmLight = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap', maxZoom: 19
            });

            // Overlay Rambu & Alur Pelayaran (OpenSeaMap — Tanpa API Key)
            var seaMarks = L.tileLayer('https://tiles.openseamap.org/seamark/{z}/{x}/{y}.png', {
                attribution: 'OpenSeaMap', maxZoom: 18, opacity: 0.9
            }).addTo(map);

            var locations = {
                nr: {lat: -5.974444, lng: 106.799167, name: "FSRU NR 1"},
                lampung: {lat: -5.441667, lng: 105.941667, name: "FSRU Lampung (PLI)"},
                jsp: {lat: -6.163611, lng: 107.74, name: "FSRU Jawa Satu"},
                priok: {lat: -6.104583, lng: 106.882506, name: "Port of Priok"}
            };
            var safeRoutes = {
                nr_lampung: [[-5.974444, 106.799167], [-5.88, 106.85], [-5.70, 106.20], [-5.441667, 105.941667]],
                nr_jsp: [[-5.974444, 106.799167], [-5.88, 106.85], [-5.85, 107.10], [-6.163611, 107.74]],
                nr_priok: [[-5.974444, 106.799167], [-6.083333, 106.883333], [-6.104583, 106.882506]],
                lampung_jsp: [[-5.441667, 105.941667], [-5.35, 106.55], [-5.85, 107.10], [-6.163611, 107.74]],
                priok_jsp: [[-6.104583, 106.882506], [-6.083333, 106.883333], [-5.88, 106.85], [-5.85, 107.10], [-6.163611, 107.74]],
                priok_lampung: [[-6.104583, 106.882506], [-6.083333, 106.883333], [-5.88, 106.85], [-5.70, 106.20], [-5.441667, 105.941667]]
            };

            var baseMarkers = L.featureGroup().addTo(map);
            Object.keys(locations).forEach(function(k) {
                var loc = locations[k];
                L.marker([loc.lat, loc.lng], {
                    icon: L.AwesomeMarkers.icon({icon:'anchor', prefix:'fa', markerColor: k==='priok'?'darkred':'cadetblue'})
                }).bindPopup('<b>' + loc.name + '</b>').addTo(baseMarkers);
            });

            var routeLayer = L.featureGroup().addTo(map);
            var polyLineBase = L.polyline([], { color: '#00e5ff', weight: 5, opacity: 0.45, className: 'route-glow' }).addTo(routeLayer);
            var polyLinePulse = L.polyline([], { color: '#e0faff', weight: 2.5, opacity: 0.95, className: 'route-pulse' }).addTo(routeLayer);

            L.control.layers(
                {
                    "🌑 Deep Navy Maritime": osmDark,
                    "🛰️ Satellite Hybrid (Esri)": esriSat,
                    "🌊 Ocean Bathymetry": esriOcean,
                    "🗺️ Street Map (Light)": osmLight
                },
                {
                    "⚓ Rambu Laut (OpenSeaMap)": seaMarks,
                    "📍 Lokasi FSRU": baseMarkers,
                    "🔵 Rute Simulasi": routeLayer
                },
                { position: 'topleft' }
            ).addTo(map);

            var markers = [], historyStack = [], redoStack = [];

            function toggleCalc() {
                var b = document.getElementById('calc_body');
                var t = document.getElementById('btn_tog');
                if (b.style.display === 'none') { b.style.display = 'block'; t.innerHTML = '−'; }
                else { b.style.display = 'none'; t.innerHTML = '+'; }
            }
            function getSnap() { return markers.map(m => ({lat: m.getLatLng().lat, lng: m.getLatLng().lng})); }
            function saveState() { historyStack.push(getSnap()); redoStack = []; if(historyStack.length>30) historyStack.shift(); }
            function performUndo() { if(!historyStack.length) return; redoStack.push(getSnap()); rebuild(historyStack.pop()); updateCalc(); }
            function performRedo() { if(!redoStack.length) return; historyStack.push(getSnap()); rebuild(redoStack.pop()); updateCalc(); }

            function createMarker(latlng) {
                var m = L.marker(latlng, { draggable: true, icon: L.AwesomeMarkers.icon({icon:'circle', prefix:'fa', markerColor:'blue'}) }).addTo(routeLayer);
                m.on('dragstart', saveState);
                m.on('dragend', updateCalc);
                m.on('contextmenu', function() {
                    if (markers.length <= 2) return;
                    saveState(); routeLayer.removeLayer(m);
                    markers = markers.filter(x => x !== m);
                    updateIcons(); updateCalc();
                });
                return m;
            }
            function updateIcons() {
                if (!markers.length) return;
                markers[0].setIcon(L.AwesomeMarkers.icon({icon:'ship', prefix:'fa', markerColor:'blue'}));
                markers[markers.length-1].setIcon(L.AwesomeMarkers.icon({icon:'flag', prefix:'fa', markerColor:'green'}));
                for (var i=1; i<markers.length-1; i++) markers[i].setIcon(L.AwesomeMarkers.icon({icon:'circle', prefix:'fa', markerColor:'orange'}));
            }
            function rebuild(coords) {
                markers.forEach(m => routeLayer.removeLayer(m));
                markers = coords.map(c => createMarker(L.latLng(c.lat || c[0], c.lng || c[1])));
                updateIcons();
            }
            function getDistNM(lat1, lon1, lat2, lon2) {
                var R=6371, dLat=(lat2-lat1)*Math.PI/180, dLon=(lon2-lon1)*Math.PI/180;
                var a=Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180)*Math.cos(lat2*Math.PI/180)*Math.sin(dLon/2)**2;
                return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)) * 0.539957;
            }
            async function fetchWeather(lat, lng) {
                var baseSpd = parseFloat(document.getElementById('inp_speed').value) || 10;
                try {
                    const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lng}&current=wind_speed_10m,wave_height&wind_speed_unit=kn`);
                    const d = await res.json();
                    let wind = d.current.wind_speed_10m || 0;
                    let wave = d.current.wave_height || (wind * 0.05);
                    document.getElementById('val_wind').innerHTML = wind.toFixed(1) + ' kn';
                    document.getElementById('val_wave').innerHTML = wave.toFixed(1) + ' m';
                    document.getElementById('live_status').innerHTML = '● Live';
                    document.getElementById('live_status').style.color = '#4ade80';
                    let pen = (wave>0.5?0.5:0) + (wave>1.5?1.5:0) + (wind>15?1.0:0);
                    document.getElementById('val_impact').innerHTML = '-' + pen.toFixed(1) + ' kn';
                    return Math.max(2, baseSpd - pen);
                } catch(e) {
                    document.getElementById('live_status').innerHTML = '● Offline';
                    document.getElementById('live_status').style.color = '#f87171';
                    return baseSpd;
                }
            }
            async function updateCalc() {
                var faktor = parseFloat(document.getElementById('inp_faktor').value) || 51.07;
                var harga = parseFloat(document.getElementById('inp_harga').value) || 17755;
                var stsJam = parseFloat(document.getElementById('inp_sts').value) || 24;
                var unit = document.getElementById('sel_unit').value;

                var path = markers.map(m => m.getLatLng());
                polyLineBase.setLatLngs(path);
                polyLinePulse.setLatLngs(path);

                var distOW = 0;
                for (var i=1; i<path.length; i++) distOW += getDistNM(path[i-1].lat, path[i-1].lng, path[i].lat, path[i].lng);
                var distPP = distOW * 2;

                var actSpd = await fetchWeather(path[0].lat, path[0].lng);
                var durPP = distPP / actSpd;
                var bbm = (unit === 'lnm') ? (distPP * faktor) : (durPP * faktor);
                var costBBM = bbm * harga;
                var costSewa = ((durPP + stsJam) / 24) * 49000000;
                var estTotal = costBBM + costSewa;

                document.getElementById('val_dist').innerHTML = distOW.toFixed(1) + ' / ' + distPP.toFixed(1) + ' NM';
                document.getElementById('val_dur').innerHTML = actSpd.toFixed(1) + ' kn (' + durPP.toFixed(1) + ' j)';
                document.getElementById('val_bbm').innerHTML = Math.round(bbm).toLocaleString('id-ID') + ' L';
                document.getElementById('val_cost_bbm').innerHTML = 'Rp ' + Math.round(costBBM).toLocaleString('id-ID');
                document.getElementById('val_cost_sewa').innerHTML = 'Rp ' + Math.round(costSewa).toLocaleString('id-ID');
                document.getElementById('val_total').innerHTML = 'Rp ' + Math.round(estTotal).toLocaleString('id-ID');
            }
            function changeRoute() {
                saveState();
                var s = document.getElementById('sel_start').value;
                var e = document.getElementById('sel_end').value;
                if (s === e) return;
                var coords = safeRoutes[s+'_'+e] || (safeRoutes[e+'_'+s] ? safeRoutes[e+'_'+s].slice().reverse() : [[locations[s].lat, locations[s].lng],[locations[e].lat, locations[e].lng]]);
                rebuild(coords);
                map.fitBounds(L.featureGroup(markers).getBounds().pad(0.22));
                updateCalc();
            }
            function addWaypoint(e) {
                saveState();
                var idx = 1, minD = Infinity;
                for (var i=0; i<markers.length-1; i++) {
                    var mid = L.latLng((markers[i].getLatLng().lat+markers[i+1].getLatLng().lat)/2, (markers[i].getLatLng().lng+markers[i+1].getLatLng().lng)/2);
                    var d = e.latlng.distanceTo(mid);
                    if (d < minD) { minD = d; idx = i+1; }
                }
                markers.splice(idx, 0, createMarker(e.latlng));
                updateIcons(); updateCalc();
            }
            polyLineBase.on('dblclick', addWaypoint);
            polyLinePulse.on('dblclick', addWaypoint);

            rebuild(safeRoutes.nr_lampung);
            map.fitBounds(L.featureGroup(markers).getBounds().pad(0.22));
            updateCalc();
        </script>
    </body>
    </html>
    """
    components.html(map_html, height=480, scrolling=True)

with col_right:
    st.markdown('<div class="panel-header">📊 Komposisi Revenue</div>', unsafe_allow_html=True)
    comp_labels = ["Biaya Sewa", "Biaya HSD"]
    comp_vals = [df["Sewa"].sum(), df["HSD_Rp"].sum()]
    comp_colors = ["#00e5ff", "#ff7b3a"]
    if include_tax:
        comp_labels.append("PBBKB 10%")
        comp_vals.append(df["PBBKB"].sum())
        comp_colors.append("#6366f1")

    fig_pie = go.Figure(go.Pie(
        labels=comp_labels, values=comp_vals, hole=0.42,
        marker=dict(colors=comp_colors, line=dict(color="#050d1a", width=2)),
        textinfo="percent", textfont=dict(color="#fff", size=11),
        hovertemplate="<b>%{label}</b><br>Rp %{value:,.0f} (%{percent})<extra></extra>"
    ))
    fig_pie.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_CLR, size=10),
        height=245, margin=dict(l=10, r=10, t=10, b=35),
        legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="panel-header">🏆 Rekor Call 2026</div>', unsafe_allow_html=True)
    if len(df) > 0:
        max_r = df.loc[df[rev_col].idxmax()]
        min_r = df.loc[df[rev_col].idxmin()]
        avg_v = df[rev_col].mean()
        st.markdown(f"""
        <div class="info-card" style="font-size:0.82rem;" tabindex="0">
            <div class="info-row" style="display:block;">
                <span style="color:#94a3b8; font-size:0.74rem;">TERTINGGI (MAX) &bull; {max_r['Bulan']}</span><br>
                <b style="color:#4ade80; font-size:0.92rem;">Rp {max_r[rev_col]:,.0f}</b>
                <span style="color:#cbd5e1; font-size:0.73rem;"> ({max_r['Kapal'].replace('TB. ','')})</span>
            </div>
            <div class="info-row" style="display:block;">
                <span style="color:#94a3b8; font-size:0.74rem;">RATA-RATA PER CALL</span><br>
                <b style="color:#00e5ff; font-size:0.92rem;">Rp {avg_v:,.0f}</b>
            </div>
            <div class="info-row" style="display:block;">
                <span style="color:#94a3b8; font-size:0.74rem;">TERENDAH (MIN) &bull; {min_r['Bulan']}</span><br>
                <b style="color:#facc15; font-size:0.92rem;">Rp {min_r[rev_col]:,.0f}</b>
                <span style="color:#cbd5e1; font-size:0.73rem;"> ({min_r['Kapal'].replace('TB. ','')})</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# BARIS 3: 3 GRAFIK BAWAH
# ==============================================================================
b1, b2, b3 = st.columns([1.05, 1.45, 1.2], gap="small")

with b1:
    st.markdown('<div class="panel-header">🎯 Panca Mutu Achievement (%)</div>', unsafe_allow_html=True)
    categories = ["Quality<br>(Avail)", "Cost<br>(Rev)", "Delivery<br>(SLA)", "Safety<br>(SOLAS)", "Morale<br>(Team)"]
    scores = [100, 100, 98, 100, 95]
    fig_radar = go.Figure(go.Scatterpolar(
        r=scores + [scores[0]], theta=categories + [categories[0]],
        fill="toself", fillcolor="rgba(255, 123, 58, 0.28)",
        line=dict(color="#ff7b3a", width=2), marker=dict(color="#00e5ff", size=5)
    ))
    fig_radar.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_CLR, size=9.5),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 105], gridcolor=GRID_CLR, tickfont=dict(size=8)),
            angularaxis=dict(gridcolor=GRID_CLR, tickfont=dict(size=9.5))
        ),
        height=275, margin=dict(l=55, r=55, t=42, b=42), showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

monthly = df.groupby(["Urutan", "Bulan"], as_index=False).agg(
    Rev=(rev_col, "sum"), Calls=("Kapal", "count")
).sort_values("Urutan")
monthly["CumRev"] = monthly["Rev"].cumsum()

with b2:
    st.markdown('<div class="panel-header">📈 Tren Pendapatan Bulanan 2026 (Juta Rp)</div>', unsafe_allow_html=True)
    max_m = (monthly["Rev"].max() / 1e6) * 1.22 if len(monthly) > 0 else 900
    fig_line = go.Figure(go.Scatter(
        x=monthly["Bulan"], y=monthly["Rev"] / 1e6,
        mode="lines+markers+text",
        line=dict(color="#00e5ff", width=2.8),
        marker=dict(color="#38bdf8", size=7, line=dict(color="#fff", width=1.2)),
        fill="tozeroy", fillcolor="rgba(0, 229, 255, 0.12)",
        text=[f"{v/1e6:.0f}Jt" for v in monthly["Rev"]],
        textposition="top center", textfont=dict(size=9, color="#7dd3fc"),
        hovertemplate="<b>%{x} 2026</b><br>Revenue: Rp %{y:,.1f} Jt<extra></extra>"
    ))
    fig_line.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_CLR, size=10),
        height=275, margin=dict(l=18, r=20, t=20, b=30),
        xaxis=dict(gridcolor=GRID_CLR, automargin=True),
        yaxis=dict(gridcolor=GRID_CLR, title="Juta Rp", range=[0, max_m], automargin=True)
    )
    st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})

with b3:
    st.markdown('<div class="panel-header">🚀 Akumulasi Revenue YTD (Miliar Rp)</div>', unsafe_allow_html=True)
    max_c = (monthly["CumRev"].max() / 1e9) * 1.22 if len(monthly) > 0 else 6
    fig_cum = go.Figure(go.Bar(
        x=monthly["Bulan"], y=monthly["CumRev"] / 1e9,
        marker=dict(color="#2563eb", line=dict(color="#00e5ff", width=1)),
        text=[f"{v/1e9:.2f}" for v in monthly["CumRev"]],
        textposition="outside", textfont=dict(size=8.5, color="#cbd5e1"),
        hovertemplate="<b>s.d. %{x} 2026</b><br>Kumulatif: Rp %{y:.2f} M<extra></extra>"
    ))
    fig_cum.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_CLR, size=10),
        height=275, margin=dict(l=18, r=20, t=20, b=30),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", tickangle=0, automargin=True),
        yaxis=dict(gridcolor=GRID_CLR, title="Miliar Rp", range=[0, max_c], automargin=True)
    )
    st.plotly_chart(fig_cum, use_container_width=True, config={"displayModeBar": False})

# ==============================================================================
# BARIS 4: MANAJEMEN DATA (INPUT CALL BARU + LIVE EDIT TABEL + EXPORT CSV)
# ==============================================================================
st.markdown('<div class="panel-header">✏️ Manajemen Data Pelayanan (Tambah, Edit &amp; Hapus Langsung)</div>', unsafe_allow_html=True)

tab_edit, tab_add = st.tabs(["📝 Edit / Hapus Data Langsung", "➕ Tambah Call Baru (Auto-Hitung)"])

with tab_edit:
    st.caption("Klik dua kali pada sel untuk mengedit angka, klik tanda (+) di baris bawah untuk menambah, atau centang baris lalu tekan Delete untuk menghapus. Klik **Simpan & Update Dashboard** agar seluruh KPI dan grafik terbarui.")

    edited_df = st.data_editor(
        st.session_state.df_data,
        num_rows="dynamic",
        use_container_width=True,
        height=340,
        column_config={
            "Bulan": st.column_config.SelectboxColumn("Bulan", options=MONTH_LIST, required=True),
            "Kapal": st.column_config.SelectboxColumn("Nama Kapal", options=VESSEL_LIST, required=True),
            "Durasi": st.column_config.NumberColumn("Durasi (Hari)", format="%.2f", min_value=0.1, step=0.05),
            "HSD_L": st.column_config.NumberColumn("HSD (Liter)", format="%d", min_value=0, step=10),
            "Harga_HSD": st.column_config.NumberColumn("Harga HSD (Rp/L)", format="Rp %d", min_value=0, step=100),
            "Sewa": st.column_config.NumberColumn("Biaya Sewa (Rp)", format="Rp %d", min_value=0, step=100000),
            "HSD_Rp": st.column_config.NumberColumn("Biaya HSD (Rp)", format="Rp %d", min_value=0, step=100000),
            "PBBKB": st.column_config.NumberColumn("PBBKB 10% (Rp)", format="Rp %d", min_value=0, step=10000),
        },
        key="editor_armakung"
    )

    btn_c1, btn_c2, btn_c3 = st.columns([1.2, 1.2, 2])
    with btn_c1:
        if st.button("💾 Simpan & Update Dashboard", type="primary", use_container_width=True):
            st.session_state.df_data = edited_df.dropna(subset=["Bulan", "Kapal"]).reset_index(drop=True)
            st.success("Dashboard berhasil diperbarui!")
            st.rerun()
    with btn_c2:
        st.download_button(
            "⬇️ Unduh Data Terbaru (CSV)",
            data=st.session_state.df_data.to_csv(index=False).encode("utf-8"),
            file_name="Data_ARMAKUNG_2026_Updated.csv",
            mime="text/csv",
            use_container_width=True
        )

with tab_add:
    st.caption("Masukkan parameter operasional kapal. Biaya Sewa (Rp 49.000.000/hari), Biaya HSD, dan PBBKB 10% akan dihitung otomatis.")
    with st.form("form_tambah_call", clear_on_submit=True):
        f1, f2, f3, f4 = st.columns(4)
        in_bulan = f1.selectbox("Bulan", MONTH_LIST, index=10)
        in_kapal = f2.selectbox("Nama Kapal", VESSEL_LIST)
        in_del = f3.text_input("Tgl Delivery", value="10/11/2026")
        in_red = f4.text_input("Tgl Re-delivery", value="13/11/2026")

        f5, f6, f7, f8 = st.columns(4)
        in_dur = f5.number_input("Durasi (Hari)", min_value=0.1, max_value=10.0, value=3.00, step=0.05)
        in_hsd_l = f6.number_input("Konsumsi HSD (Liter)", min_value=0, max_value=20000, value=7800, step=100)
        in_hrg = f7.number_input("Harga HSD (Rp/Liter)", min_value=0, max_value=50000, value=17755, step=100)
        in_tarif = f8.number_input("Tarif Sewa (Rp/Hari)", min_value=0, max_value=100000000, value=49000000, step=500000)

        if st.form_submit_button("➕ Tambahkan Call ke Dashboard", type="primary", use_container_width=True):
            calc_sewa = round(in_dur * in_tarif)
            calc_hsd = round(in_hsd_l * in_hrg)
            calc_pbbkb = round(calc_hsd * 0.10)
            new_row = pd.DataFrame([{
                "Bulan": in_bulan, "Kapal": in_kapal,
                "Delivery": in_del, "Redelivery": in_red,
                "Durasi": in_dur, "HSD_L": in_hsd_l, "Harga_HSD": in_hrg,
                "Sewa": calc_sewa, "HSD_Rp": calc_hsd, "PBBKB": calc_pbbkb
            }])
            st.session_state.df_data = pd.concat([st.session_state.df_data, new_row], ignore_index=True)
            st.success(f"Call baru ({in_kapal} - {in_bulan}) berhasil ditambahkan!")
            st.rerun()
