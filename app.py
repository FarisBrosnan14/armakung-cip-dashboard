import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go

# ==============================================================================
# KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="ARMAKUNG Maritime Command Center 2026",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# CUSTOM CSS: DARK COMMAND CENTER THEME (NEON CYAN & AMBER)
# ==============================================================================
st.markdown("""
<style>
    /* Background utama dark navy */
    .stApp {
        background: radial-gradient(circle at top center, #0d2240 0%, #050d1a 70%);
        color: #e2e8f0;
    }
    header[data-testid="stHeader"] {
        background: rgba(5, 13, 26, 0.85);
    }
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 1.5rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    /* Header Command Center */
    .cmd-title-wrap {
        text-align: center;
        padding: 0.4rem 0 0.8rem 0;
        border-bottom: 2px solid rgba(0, 229, 255, 0.45);
        margin-bottom: 1rem;
        position: relative;
    }
    .cmd-title {
        font-family: 'Segoe UI', sans-serif;
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: 2px;
        color: #38e8ff;
        text-shadow: 0 0 18px rgba(0, 229, 255, 0.65);
        margin: 0;
    }
    .cmd-subtitle {
        font-size: 0.85rem;
        color: #94a3b8;
        letter-spacing: 1px;
        margin-top: 4px;
    }

    /* 3 Kartu KPI Atas dengan sudut chamfered & angka oranye menyala */
    .kpi-box {
        background: linear-gradient(135deg, rgba(13, 35, 66, 0.88), rgba(7, 20, 40, 0.92));
        border: 1px solid rgba(0, 229, 255, 0.55);
        box-shadow: inset 0 0 15px rgba(0, 229, 255, 0.12), 0 0 12px rgba(0, 229, 255, 0.18);
        border-radius: 6px;
        padding: 0.85rem 1.2rem;
        margin-bottom: 0.9rem;
    }
    .kpi-label {
        font-size: 0.88rem;
        font-weight: 600;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .kpi-value-row {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        margin-top: 4px;
    }
    .kpi-val {
        font-size: 1.85rem;
        font-weight: 800;
        color: #ff7b3a;
        text-shadow: 0 0 12px rgba(255, 123, 58, 0.45);
    }
    .kpi-unit {
        font-size: 0.82rem;
        color: #7dd3fc;
        font-weight: 600;
    }

    /* Panel Container Border Cyan */
    .panel-header {
        background: linear-gradient(90deg, rgba(0, 229, 255, 0.18), transparent);
        border-left: 3px solid #00e5ff;
        padding: 5px 10px;
        font-size: 0.95rem;
        font-weight: 700;
        color: #67e8f9;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    /* Sidebar dark */
    section[data-testid="stSidebar"] {
        background-color: #071326;
        border-right: 1px solid rgba(0, 229, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA AKTUAL 2026 (JANUARI – OKTOBER 2026, 19 CALL)
# ==============================================================================
INITIAL_DATA = [
    {"Bulan": "Jan", "Urutan": 1, "Kapal": "TB. AQUA HARBOUR", "Delivery": "31/01/2026", "Redelivery": "03/02/2026", "Durasi": 3.43, "HSD_L": 8307, "Harga_HSD": 19375, "Sewa": 168233333, "HSD_Rp": 160948125, "PBBKB": 15513323},
    {"Bulan": "Feb", "Urutan": 2, "Kapal": "TB. MEDELIN CITRA", "Delivery": "15/02/2026", "Redelivery": "18/02/2026", "Durasi": 2.98, "HSD_L": 8424, "Harga_HSD": 19375, "Sewa": 146183333, "HSD_Rp": 163215000, "PBBKB": 15731820},
    {"Bulan": "Feb", "Urutan": 2, "Kapal": "TB. AQUA HARBOUR", "Delivery": "24/02/2026", "Redelivery": "27/02/2026", "Durasi": 3.38, "HSD_L": 7978, "Harga_HSD": 19555, "Sewa": 165375000, "HSD_Rp": 156009790, "PBBKB": 15042519},
    {"Bulan": "Mar", "Urutan": 3, "Kapal": "TB. MEDELIN CITRA", "Delivery": "08/03/2026", "Redelivery": "11/03/2026", "Durasi": 2.72, "HSD_L": 8107, "Harga_HSD": 19555, "Sewa": 133320833, "HSD_Rp": 158532385, "PBBKB": 15285749},
    {"Bulan": "Mar", "Urutan": 3, "Kapal": "TB. AQUA HARBOUR", "Delivery": "14/03/2026", "Redelivery": "17/03/2026", "Durasi": 3.35, "HSD_L": 8452, "Harga_HSD": 19555, "Sewa": 164354167, "HSD_Rp": 165278860, "PBBKB": 15936246},
    {"Bulan": "Apr", "Urutan": 4, "Kapal": "TB. MEDELIN CITRA", "Delivery": "04/04/2026", "Redelivery": "07/04/2026", "Durasi": 2.55, "HSD_L": 8363, "Harga_HSD": 19825, "Sewa": 125052083, "HSD_Rp": 165796475, "PBBKB": 15994238},
    {"Bulan": "Apr", "Urutan": 4, "Kapal": "TB. AQUA HARBOUR", "Delivery": "09/04/2026", "Redelivery": "12/04/2026", "Durasi": 3.15, "HSD_L": 8031, "Harga_HSD": 19825, "Sewa": 154554167, "HSD_Rp": 159214575, "PBBKB": 15359288},
    {"Bulan": "Mei", "Urutan": 5, "Kapal": "TB. AQUA HARBOUR", "Delivery": "03/05/2026", "Redelivery": "06/05/2026", "Durasi": 3.32, "HSD_L": 8039, "Harga_HSD": 28195, "Sewa": 162720833, "HSD_Rp": 226659605, "PBBKB": 22103231},
    {"Bulan": "Mei", "Urutan": 5, "Kapal": "TB. MEDELIN CITRA", "Delivery": "29/05/2026", "Redelivery": "01/06/2026", "Durasi": 3.35, "HSD_L": 8700, "Harga_HSD": 24415, "Sewa": 164150000, "HSD_Rp": 212410500, "PBBKB": 20632050},
    {"Bulan": "Jun", "Urutan": 6, "Kapal": "TB. MEDELIN CITRA", "Delivery": "22/06/2026", "Redelivery": "24/06/2026", "Durasi": 1.29, "HSD_L": 7144, "Harga_HSD": 24415, "Sewa": 63291667, "HSD_Rp": 174420760, "PBBKB": 16941996},
    {"Bulan": "Jul", "Urutan": 7, "Kapal": "TB. AQUA HARBOUR", "Delivery": "04/07/2026", "Redelivery": "07/07/2026", "Durasi": 2.73, "HSD_L": 7914, "Harga_HSD": 23245, "Sewa": 133933333, "HSD_Rp": 183960930, "PBBKB": 17842113},
    {"Bulan": "Jul", "Urutan": 7, "Kapal": "TB. MEDELIN PARTNER", "Delivery": "08/07/2026", "Redelivery": "09/07/2026", "Durasi": 1.41, "HSD_L": 3660, "Harga_HSD": 23245, "Sewa": 69008333, "HSD_Rp": 85076700, "PBBKB": 8251470},
    {"Bulan": "Jul", "Urutan": 7, "Kapal": "TB. MEDELIN PARTNER", "Delivery": "19/07/2026", "Redelivery": "21/07/2026", "Durasi": 1.66, "HSD_L": 3999, "Harga_HSD": 23245, "Sewa": 81258333, "HSD_Rp": 92956755, "PBBKB": 9015746},
    {"Bulan": "Agt", "Urutan": 8, "Kapal": "TB. AQUA HARBOUR", "Delivery": "10/08/2026", "Redelivery": "13/08/2026", "Durasi": 2.14, "HSD_L": 7062, "Harga_HSD": 17080, "Sewa": 104737500, "HSD_Rp": 120618960, "PBBKB": 11567556},
    {"Bulan": "Agt", "Urutan": 8, "Kapal": "TB. MEDELIN CITRA", "Delivery": "24/08/2026", "Redelivery": "26/08/2026", "Durasi": 1.59, "HSD_L": 7708, "Harga_HSD": 17080, "Sewa": 77991667, "HSD_Rp": 131652640, "PBBKB": 12625704},
    {"Bulan": "Sep", "Urutan": 9, "Kapal": "TB. MEDELIN PARTNER", "Delivery": "08/09/2026", "Redelivery": "10/09/2026", "Durasi": 1.65, "HSD_L": 4238, "Harga_HSD": 17080, "Sewa": 80645833, "HSD_Rp": 72385040, "PBBKB": 6941844},
    {"Bulan": "Sep", "Urutan": 9, "Kapal": "TB. AQUA HARBOUR", "Delivery": "20/09/2026", "Redelivery": "23/09/2026", "Durasi": 3.11, "HSD_L": 7381, "Harga_HSD": 17755, "Sewa": 152512500, "HSD_Rp": 131049655, "PBBKB": 12588296},
    {"Bulan": "Sep", "Urutan": 9, "Kapal": "TB. MEDELIN PARTNER", "Delivery": "29/09/2026", "Redelivery": "01/10/2026", "Durasi": 1.65, "HSD_L": 4205, "Harga_HSD": 17755, "Sewa": 81054167, "HSD_Rp": 74659775, "PBBKB": 7171628},
    {"Bulan": "Okt", "Urutan": 10, "Kapal": "TB. MEDELIN PARTNER", "Delivery": "23/10/2026", "Redelivery": "25/10/2026", "Durasi": 1.60, "HSD_L": 4050, "Harga_HSD": 17755, "Sewa": 78604167, "HSD_Rp": 71907750, "PBBKB": 6907275},
]

if "records" not in st.session_state:
    st.session_state.records = INITIAL_DATA.copy()

# ==============================================================================
# SIDEBAR: FILTER & SIMULATOR CALL REAL-TIME
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Kontrol Command Center")
    basis_pajak = st.radio(
        "Basis Perhitungan:",
        ["Tanpa Pajak (Sewa + HSD)", "Grand Total (Incl. PBBKB 10%)"],
        index=0
    )
    include_tax = basis_pajak == "Grand Total (Incl. PBBKB 10%)"

    df_all = pd.DataFrame(st.session_state.records)
    df_all["Tanpa_Pajak"] = df_all["Sewa"] + df_all["HSD_Rp"]
    df_all["Grand_Total"] = df_all["Tanpa_Pajak"] + df_all["PBBKB"]
    df_all["Kategori"] = df_all["Durasi"].apply(lambda x: "Full Service" if x > 2.0 else "Berthing Only")

    sel_vessels = st.multiselect("Armada Tugboat:", sorted(df_all["Kapal"].unique()), default=sorted(df_all["Kapal"].unique()))
    sel_cats = st.multiselect("Kategori Layanan:", ["Full Service", "Berthing Only"], default=["Full Service", "Berthing Only"])

    st.divider()
    st.markdown("### ➕ Tambah Simulasi Call")
    with st.form("sim_call"):
        s_bln = st.selectbox("Bulan", ["Nov", "Des"])
        s_kpl = st.selectbox("Kapal", ["TB. AQUA HARBOUR", "TB. MEDELIN CITRA", "TB. MEDELIN PARTNER"])
        s_dur = st.number_input("Durasi (Hari)", 1.0, 5.0, 3.0, 0.1)
        s_hsd = st.number_input("HSD (Liter)", 2000, 12000, 7800, 100)
        s_hrg = st.number_input("Harga HSD (Rp/L)", 15000, 35000, 18000, 250)
        if st.form_submit_button("Simulasikan", use_container_width=True):
            sewa_v = round(s_dur * 49_000_000)
            hsd_v = round(s_hsd * s_hrg)
            st.session_state.records.append({
                "Bulan": s_bln, "Urutan": 11 if s_bln == "Nov" else 12,
                "Kapal": s_kpl, "Delivery": f"Sim ({s_bln} 26)", "Redelivery": "-",
                "Durasi": s_dur, "HSD_L": s_hsd, "Harga_HSD": s_hrg,
                "Sewa": sewa_v, "HSD_Rp": hsd_v, "PBBKB": round(hsd_v * 0.10)
            })
            st.rerun()

    if len(st.session_state.records) > len(INITIAL_DATA):
        if st.button("🔄 Reset ke 19 Call Aktual", use_container_width=True):
            st.session_state.records = INITIAL_DATA.copy()
            st.rerun()

# Filter data
df = df_all[(df_all["Kapal"].isin(sel_vessels)) & (df_all["Kategori"].isin(sel_cats))].copy()
rev_col = "Grand_Total" if include_tax else "Tanpa_Pajak"
active_months = max(10, int(df_all["Urutan"].max()))
prorata = 12 / active_months

total_rev = df[rev_col].sum()
proj_rev = total_rev * prorata
total_calls = len(df)
ann_calls = total_calls * prorata
full_df = df[df["Durasi"] > 2.0]
potensi_rev = (full_df[rev_col].mean() * ann_calls) if len(full_df) > 0 else proj_rev

# ==============================================================================
# HEADER COMMAND CENTER
# ==============================================================================
st.markdown("""
<div class="cmd-title-wrap">
    <div class="cmd-title">ARMAKUNG MARITIME MONITORING &amp; FUEL COMMAND CENTER</div>
    <div class="cmd-subtitle">PT NUSANTARA REGAS &bull; SINERGI TUGBOAT ON-CALL PERTAMINA GROUP &bull; ZERO CAPEX VALUE CREATION 2026</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# BARIS 1: 3 KARTU KPI UTAMA
# ==============================================================================
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">Realisasi Revenue YTD ({active_months} Bulan)</div>
        <div class="kpi-value-row">
            <span class="kpi-val">{total_rev/1e9:,.2f} Miliar</span>
            <span class="kpi-unit">IDR &bull; {total_calls} Call Aktual</span>
        </div>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">Proyeksi 1 Tahun Anggaran (12/{active_months})</div>
        <div class="kpi-value-row">
            <span class="kpi-val">{proj_rev/1e9:,.2f} Miliar</span>
            <span class="kpi-unit">IDR &bull; {ann_calls:.1f} Call/Thn</span>
        </div>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">Potensi Full Service 2026</div>
        <div class="kpi-value-row">
            <span class="kpi-val">{potensi_rev/1e9:,.2f} Miliar</span>
            <span class="kpi-unit">IDR &bull; Zero CAPEX</span>
        </div>
    </div>""", unsafe_allow_html=True)

# Helper template Plotly dark transparan
PLOT_BG = "rgba(8, 22, 44, 0.72)"
FONT_CLR = "#cbd5e1"
GRID_CLR = "rgba(0, 229, 255, 0.14)"

# ==============================================================================
# BARIS 2: KIRI (ARMADA) | TENGAH (PETA & KALKULATOR BBM LIVE) | KANAN (PIE)
# ==============================================================================
col_left, col_mid, col_right = st.columns([1.15, 2.3, 1.15], gap="small")

with col_left:
    st.markdown('<div class="panel-header">⚓ Revenue per Armada (Miliar Rp)</div>', unsafe_allow_html=True)
    v_agg = df.groupby("Kapal", as_index=False).agg(Rev=(rev_col, "sum"), Calls=("Bulan", "count"), Durasi=("Durasi", "sum")).sort_values("Rev")
    fig_hbar = go.Figure(go.Bar(
        x=v_agg["Rev"] / 1e9,
        y=v_agg["Kapal"].str.replace("TB. ", ""),
        orientation="h",
        marker=dict(color=["#38bdf8", "#6366f1", "#00e5ff"], line=dict(color="#00e5ff", width=1)),
        text=[f"Rp {r/1e9:.2f} M ({c}x)" for r, c in zip(v_agg["Rev"], v_agg["Calls"])],
        textposition="inside",
        insidetextfont=dict(color="#041020", size=11, family="Segoe UI"),
        hovertemplate="<b>%{y}</b><br>Revenue: Rp %{x:.2f} M<extra></extra>"
    ))
    fig_hbar.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_CLR, size=11),
        height=240, margin=dict(l=10, r=15, t=10, b=25),
        xaxis=dict(gridcolor=GRID_CLR, title="Miliar Rp"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)")
    )
    st.plotly_chart(fig_hbar, use_container_width=True)

    st.markdown('<div class="panel-header">⏱️ Ringkasan Operasional YTD</div>', unsafe_allow_html=True)
    total_jam = df["Durasi"].sum() * 24
    total_hsd = df["HSD_L"].sum()
    st.markdown(f"""
    <div style="background:{PLOT_BG}; border:1px solid rgba(0,229,255,0.3); border-radius:6px; padding:12px; font-size:0.86rem;">
        <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.08);">
            <span style="color:#94a3b8;">Total Durasi Layanan</span>
            <b style="color:#00e5ff;">{df['Durasi'].sum():.2f} Hari ({total_jam:,.0f} Jam)</b>
        </div>
        <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.08);">
            <span style="color:#94a3b8;">Total Konsumsi HSD</span>
            <b style="color:#ffeb3b;">{total_hsd:,.0f} Liter</b>
        </div>
        <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.08);">
            <span style="color:#94a3b8;">Full Service vs Partial</span>
            <b style="color:#4ade80;">{len(full_df)} Full / {len(df)-len(full_df)} Partial</b>
        </div>
        <div style="display:flex; justify-content:space-between; padding:6px 0;">
            <span style="color:#94a3b8;">Lead Time Saving</span>
            <b style="color:#ff7b3a;">52,13 Jam (748% Lebih Cepat)</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_mid:
    st.markdown('<div class="panel-header">🗺️ Live Maritime Route &amp; Fuel Calculator (NR OptiVoyage)</div>', unsafe_allow_html=True)

    # Embedded Leaflet Dark Map + Fuel & Charter Cost Calculator (dari Peta_Final_NR_Fuel)
    map_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css"/>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css"/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>
        <script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>
        <style>
            html, body, #map { width:100%; height:100%; margin:0; padding:0; background:#050d1a; font-family:'Segoe UI',sans-serif; }
            .calc-panel {
                position: fixed; top: 10px; right: 10px; width: 285px;
                background: rgba(10, 22, 42, 0.93); color: #fff; z-index: 9999;
                border: 1px solid #00e5ff; border-radius: 8px;
                box-shadow: 0 0 18px rgba(0, 229, 255, 0.28); backdrop-filter: blur(6px);
                overflow: hidden;
            }
            .calc-hdr {
                background: linear-gradient(90deg, #0b2545, #133c6e); padding: 7px 10px;
                display:flex; justify-content:space-between; align-items:center;
                border-bottom: 2px solid #00e5ff; cursor: pointer;
            }
            .calc-body { padding: 10px; max-height: 390px; overflow-y: auto; font-size: 11px; }
            .cfg-box { background: rgba(0,229,255,0.08); border:1px solid rgba(0,229,255,0.4); border-radius:5px; padding:7px; margin-bottom:7px; }
            .row2 { display:flex; justify-content:space-between; gap:6px; margin-top:4px; }
            input, select {
                background:#061124; color:#fff; border:1px solid #334155; border-radius:3px;
                padding:3px 5px; font-size:11px; width:100%; box-sizing:border-box;
            }
            .wx-box { background: rgba(0,0,0,0.35); border:1px solid #334155; border-radius:5px; padding:6px; margin-bottom:7px; }
            .wx-grid { display:flex; justify-content:space-between; text-align:center; margin-top:4px; }
            .btn-sm { border:none; border-radius:3px; padding:4px 6px; font-size:10px; font-weight:700; cursor:pointer; }
            table { width:100%; border-collapse:collapse; margin-top:6px; font-size:11px; }
            td { padding:4px 3px; border-bottom:1px solid rgba(255,255,255,0.1); }
            .val { text-align:right; font-weight:700; }
        </style>
    </head>
    <body>
        <div id="map"></div>
        <div class="calc-panel">
            <div class="calc-hdr" onclick="toggleCalc()">
                <span style="color:#00e5ff; font-weight:800; font-size:12px;">⛽ NR FUEL &amp; CHARTER CALC</span>
                <span id="btn_tog" style="color:#fff; font-weight:bold;">−</span>
            </div>
            <div id="calc_body" class="calc-body">
                <div class="cfg-box">
                    <div class="row2">
                        <div style="flex:1;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <label style="font-size:9px; color:#94a3b8;">Fuel Rate</label>
                                <select id="sel_unit" onchange="updateCalc()" style="width:auto; font-size:9px; padding:1px 2px; color:#00e5ff;">
                                    <option value="lnm">L/NM</option>
                                    <option value="lhr">L/Hr</option>
                                </select>
                            </div>
                            <input type="number" id="inp_faktor" value="51.07" step="0.1" oninput="updateCalc()">
                        </div>
                        <div style="flex:1;">
                            <label style="font-size:9px; color:#94a3b8;">Speed (Knot)</label>
                            <input type="number" id="inp_speed" value="10.0" step="0.5" oninput="updateCalc()">
                        </div>
                    </div>
                    <div class="row2">
                        <div style="flex:1;">
                            <label style="font-size:9px; color:#94a3b8;">Harga HSD (Rp/L)</label>
                            <input type="number" id="inp_harga" value="17755" step="100" oninput="updateCalc()">
                        </div>
                        <div style="flex:1;">
                            <label style="font-size:9px; color:#94a3b8;">Standby STS (Jam)</label>
                            <input type="number" id="inp_sts" value="24" step="2" oninput="updateCalc()">
                        </div>
                    </div>
                </div>

                <div class="wx-box">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#00e5ff; font-size:10px; font-weight:700;">☁️ LIVE WEATHER</span>
                        <span id="live_status" style="font-size:9px; color:#94a3b8;">● Connecting...</span>
                    </div>
                    <div class="wx-grid">
                        <div><div style="color:#94a3b8;font-size:9px;">Wind</div><div id="val_wind">-- kn</div></div>
                        <div><div style="color:#94a3b8;font-size:9px;">Wave</div><div id="val_wave">-- m</div></div>
                        <div><div style="color:#94a3b8;font-size:9px;">Impact</div><div id="val_impact" style="color:#ffeb3b;">-- kn</div></div>
                    </div>
                </div>

                <div class="row2" style="margin-bottom:6px;">
                    <div style="flex:1;">
                        <label style="font-size:9px; color:#94a3b8;">FROM</label>
                        <select id="sel_start" onchange="changeRoute()">
                            <option value="nr" selected>FSRU NR 1</option>
                            <option value="lampung">FSRU Lampung</option>
                            <option value="jsp">FSRU Jawa Satu</option>
                            <option value="priok">Port of Priok</option>
                        </select>
                    </div>
                    <div style="flex:1;">
                        <label style="font-size:9px; color:#94a3b8;">TO</label>
                        <select id="sel_end" onchange="changeRoute()">
                            <option value="lampung" selected>FSRU Lampung</option>
                            <option value="jsp">FSRU Jawa Satu</option>
                            <option value="priok">Port of Priok</option>
                            <option value="nr">FSRU NR 1</option>
                        </select>
                    </div>
                </div>

                <div class="row2" style="margin-bottom:4px;">
                    <button class="btn-sm" onclick="performUndo()" style="flex:1; background:#facc15; color:#000;">↩ UNDO</button>
                    <button class="btn-sm" onclick="performRedo()" style="flex:1; background:#22c55e; color:#fff;">REDO ↪</button>
                    <button class="btn-sm" onclick="changeRoute()" style="flex:1; background:#ef4444; color:#fff;">RESET</button>
                </div>

                <table>
                    <tr><td style="color:#94a3b8;">Jarak One Way / PP</td><td id="val_dist" class="val">--</td></tr>
                    <tr><td style="color:#94a3b8;">Actual Speed</td><td id="val_spd" class="val" style="color:#00e5ff;">--</td></tr>
                    <tr><td style="color:#94a3b8;">Durasi Sailing (PP)</td><td id="val_dur" class="val">--</td></tr>
                    <tr><td style="color:#94a3b8;">Estimasi Total BBM</td><td id="val_bbm" class="val" style="color:#ffeb3b;">--</td></tr>
                    <tr><td style="color:#94a3b8;">Biaya BBM (HSD)</td><td id="val_cost_bbm" class="val">--</td></tr>
                    <tr><td style="color:#94a3b8;">Sewa (Rp 49 Jt/hr)</td><td id="val_cost_sewa" class="val">--</td></tr>
                    <tr style="background:rgba(0,229,255,0.14);">
                        <td style="color:#00e5ff; font-weight:800;">EST. TOTAL (NET)</td>
                        <td id="val_total" class="val" style="color:#ff7b3a; font-size:12px;">--</td>
                    </tr>
                </table>
                <div style="font-size:9px; color:#64748b; text-align:center; margin-top:5px;">
                    Drag marker &bull; Double-click garis: tambah titik &bull; Klik kanan: hapus
                </div>
            </div>
        </div>

        <script>
            var map = L.map('map', { center: [-5.75, 106.45], zoom: 8, doubleClickZoom: false });
            var darkTile = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', { attribution: 'Esri Dark' }).addTo(map);
            var lightTile = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', { attribution: 'Esri Street' });

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
            var polyLine = L.polyline([], { color: '#00e5ff', weight: 4, opacity: 0.9 }).addTo(routeLayer);
            L.control.layers({"Dark Map": darkTile, "Light Map": lightTile}, {"Lokasi FSRU": baseMarkers, "Rute Simulasi": routeLayer}, {position:'topleft'}).addTo(map);

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
                    document.getElementById('live_status').innerHTML = '● Online';
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
                polyLine.setLatLngs(path);
                var distOW = 0;
                for (var i=1; i<path.length; i++) distOW += getDistNM(path[i-1].lat, path[i-1].lng, path[i].lat, path[i].lng);
                var distPP = distOW * 2;

                var actSpd = await fetchWeather(path[0].lat, path[0].lng);
                var durPP = distPP / actSpd;
                var bbm = (unit === 'lnm') ? (distPP * faktor) : (durPP * faktor);
                var costBBM = bbm * harga;
                var totalHari = (durPP + stsJam) / 24;
                var costSewa = totalHari * 49000000;
                var estTotal = costBBM + costSewa;

                document.getElementById('val_dist').innerHTML = distOW.toFixed(1) + ' / ' + distPP.toFixed(1) + ' NM';
                document.getElementById('val_spd').innerHTML = actSpd.toFixed(1) + ' kn';
                document.getElementById('val_dur').innerHTML = durPP.toFixed(1) + ' Jam';
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
                map.fitBounds(L.featureGroup(markers).getBounds().pad(0.18));
                updateCalc();
            }

            polyLine.on('dblclick', function(e) {
                saveState();
                var idx = 1, minD = Infinity;
                for (var i=0; i<markers.length-1; i++) {
                    var mid = L.latLng((markers[i].getLatLng().lat+markers[i+1].getLatLng().lat)/2, (markers[i].getLatLng().lng+markers[i+1].getLatLng().lng)/2);
                    var d = e.latlng.distanceTo(mid);
                    if (d < minD) { minD = d; idx = i+1; }
                }
                markers.splice(idx, 0, createMarker(e.latlng));
                updateIcons(); updateCalc();
            });

            rebuild(safeRoutes.nr_lampung);
            map.fitBounds(L.featureGroup(markers).getBounds().pad(0.18));
            updateCalc();
        </script>
    </body>
    </html>
    """
    components.html(map_html, height=470)

with col_right:
    st.markdown('<div class="panel-header">📊 Komposisi Revenue</div>', unsafe_allow_html=True)
    comp_labels = ["Biaya Sewa Kapal", "Biaya BBM (HSD)"]
    comp_vals = [df["Sewa"].sum(), df["HSD_Rp"].sum()]
    comp_colors = ["#00e5ff", "#ff7b3a"]
    if include_tax:
        comp_labels.append("Pajak PBBKB 10%")
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
        height=240, margin=dict(l=10, r=10, t=10, b=35),
        legend=dict(orientation="h", yanchor="top", y=-0.05, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('<div class="panel-header">🏆 Rekor Call 2026 (Net)</div>', unsafe_allow_html=True)
    if len(df) > 0:
        max_r = df.loc[df[rev_col].idxmax()]
        min_r = df.loc[df[rev_col].idxmin()]
        avg_v = df[rev_col].mean()
        st.markdown(f"""
        <div style="background:{PLOT_BG}; border:1px solid rgba(0,229,255,0.3); border-radius:6px; padding:12px; font-size:0.84rem;">
            <div style="margin-bottom:8px;">
                <span style="color:#94a3b8; font-size:0.78rem;">TERTINGGI (MAX) &bull; {max_r['Bulan']}</span><br>
                <b style="color:#4ade80; font-size:0.95rem;">Rp {max_r[rev_col]:,.0f}</b>
                <span style="color:#cbd5e1; font-size:0.75rem;"> ({max_r['Kapal'].replace('TB. ','')})</span>
            </div>
            <div style="margin-bottom:8px;">
                <span style="color:#94a3b8; font-size:0.78rem;">RATA-RATA PER CALL</span><br>
                <b style="color:#00e5ff; font-size:0.95rem;">Rp {avg_v:,.0f}</b>
            </div>
            <div>
                <span style="color:#94a3b8; font-size:0.78rem;">TERENDAH (MIN) &bull; {min_r['Bulan']}</span><br>
                <b style="color:#facc15; font-size:0.95rem;">Rp {min_r[rev_col]:,.0f}</b>
                <span style="color:#cbd5e1; font-size:0.75rem;"> ({min_r['Kapal'].replace('TB. ','')})</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# BARIS 3: 3 GRAFIK ANALITIK BAWAH (RADAR | LINE TREND | ACCUMULATED BAR)
# ==============================================================================
st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
b1, b2, b3 = st.columns([1.05, 1.45, 1.15], gap="small")

with b1:
    st.markdown('<div class="panel-header">🎯 Panca Mutu Achievement (%)</div>', unsafe_allow_html=True)
    categories = ["Quality (Avail)", "Cost (Revenue)", "Delivery (SLA)", "Safety (SOLAS)", "Morale (Team)"]
    scores = [100, 100, 98, 100, 95]
    fig_radar = go.Figure(go.Scatterpolar(
        r=scores + [scores[0]], theta=categories + [categories[0]],
        fill="toself", fillcolor="rgba(255, 123, 58, 0.28)",
        line=dict(color="#ff7b3a", width=2), marker=dict(color="#00e5ff", size=5)
    ))
    fig_radar.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_CLR, size=10),
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor=GRID_CLR, tickfont=dict(size=8)),
            angularaxis=dict(gridcolor=GRID_CLR)
        ),
        height=240, margin=dict(l=40, r=40, t=20, b=20), showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True)

monthly = df.groupby(["Urutan", "Bulan"], as_index=False).agg(
    Rev=(rev_col, "sum"), Calls=("Kapal", "count"), HSD=("HSD_L", "sum")
).sort_values("Urutan")
monthly["CumRev"] = monthly["Rev"].cumsum()

with b2:
    st.markdown('<div class="panel-header">📈 Tren Pendapatan Bulanan 2026 (Juta Rp)</div>', unsafe_allow_html=True)
    fig_line = go.Figure(go.Scatter(
        x=monthly["Bulan"], y=monthly["Rev"] / 1e6,
        mode="lines+markers+text",
        line=dict(color="#00e5ff", width=3),
        marker=dict(color="#38bdf8", size=8, line=dict(color="#fff", width=1.5)),
        fill="tozeroy", fillcolor="rgba(0, 229, 255, 0.12)",
        text=[f"{v/1e6:.0f}Jt" for v in monthly["Rev"]],
        textposition="top center", textfont=dict(size=9, color="#7dd3fc"),
        hovertemplate="<b>%{x} 2026</b><br>Revenue: Rp %{y:,.1f} Jt<extra></extra>"
    ))
    fig_line.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_CLR, size=10),
        height=240, margin=dict(l=15, r=15, t=20, b=25),
        xaxis=dict(gridcolor=GRID_CLR),
        yaxis=dict(gridcolor=GRID_CLR, title="Juta Rp")
    )
    st.plotly_chart(fig_line, use_container_width=True)

with b3:
    st.markdown('<div class="panel-header">🚀 Akumulasi Revenue YTD (Miliar Rp)</div>', unsafe_allow_html=True)
    fig_cum = go.Figure(go.Bar(
        x=monthly["Bulan"], y=monthly["CumRev"] / 1e9,
        marker=dict(color="#2563eb", line=dict(color="#00e5ff", width=1)),
        text=[f"{v/1e9:.2f}" for v in monthly["CumRev"]],
        textposition="outside", textfont=dict(size=9, color="#cbd5e1"),
        hovertemplate="<b>s.d. %{x} 2026</b><br>Kumulatif: Rp %{y:.2f} M<extra></extra>"
    ))
    fig_cum.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_CLR, size=10),
        height=240, margin=dict(l=15, r=15, t=22, b=25),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(gridcolor=GRID_CLR, title="Miliar Rp", range=[0, max(6, (monthly["CumRev"].max()/1e9)*1.18) if len(monthly) else 6])
    )
    st.plotly_chart(fig_cum, use_container_width=True)

# ==============================================================================
# BARIS 4: EXPANDER TABEL BREAKDOWN & EKSPOR CSV
# ==============================================================================
with st.expander("📋 Lihat Rincian 19 Call Pelayanan 2026 & Unduh CSV"):
    disp_cols = ["Bulan", "Kapal", "Delivery", "Redelivery", "Durasi", "Kategori", "HSD_L", "Sewa", "HSD_Rp", "Tanpa_Pajak", "PBBKB", "Grand_Total"]
    st.dataframe(
        df[disp_cols].style.format({
            "Durasi": "{:.2f} hr", "HSD_L": "{:,.0f} L",
            "Sewa": "Rp {:,.0f}", "HSD_Rp": "Rp {:,.0f}",
            "Tanpa_Pajak": "Rp {:,.0f}", "PBBKB": "Rp {:,.0f}", "Grand_Total": "Rp {:,.0f}"
        }),
        use_container_width=True, height=340
    )
    st.download_button(
        "⬇️ Unduh Rekap CSV",
        data=df[disp_cols].to_csv(index=False).encode("utf-8"),
        file_name="Rekap_ARMAKUNG_2026.csv",
        mime="text/csv"
    )
