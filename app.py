import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="Dashboard Monitoring ARMAKUNG 2026",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan eksekutif
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1B365D 0%, #2C5282 100%);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 1.8rem;
    }
    .main-header p {
        color: #E2E8F0;
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }
    div[data-testid="stMetric"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #1B365D;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA AKTUAL 2026 (JANUARI - OKTOBER 2026, 19 CALL)
# Catatan: Transaksi Des 2025 dikecualikan sesuai asas fairness 1 tahun anggaran
# ==============================================================================
INITIAL_DATA = [
    {"Bulan": "Jan 2026", "Urutan": 1, "Kapal": "TB. AQUA HARBOUR", "Delivery": "31/01/2026", "Redelivery": "03/02/2026", "Durasi": 3.43, "HSD_L": 8307, "Harga_HSD": 19375, "Sewa": 168233333, "HSD_Rp": 160948125, "PBBKB": 15513323},
    {"Bulan": "Feb 2026", "Urutan": 2, "Kapal": "TB. MEDELIN CITRA", "Delivery": "15/02/2026", "Redelivery": "18/02/2026", "Durasi": 2.98, "HSD_L": 8424, "Harga_HSD": 19375, "Sewa": 146183333, "HSD_Rp": 163215000, "PBBKB": 15731820},
    {"Bulan": "Feb 2026", "Urutan": 2, "Kapal": "TB. AQUA HARBOUR", "Delivery": "24/02/2026", "Redelivery": "27/02/2026", "Durasi": 3.38, "HSD_L": 7978, "Harga_HSD": 19555, "Sewa": 165375000, "HSD_Rp": 156009790, "PBBKB": 15042519},
    {"Bulan": "Mar 2026", "Urutan": 3, "Kapal": "TB. MEDELIN CITRA", "Delivery": "08/03/2026", "Redelivery": "11/03/2026", "Durasi": 2.72, "HSD_L": 8107, "Harga_HSD": 19555, "Sewa": 133320833, "HSD_Rp": 158532385, "PBBKB": 15285749},
    {"Bulan": "Mar 2026", "Urutan": 3, "Kapal": "TB. AQUA HARBOUR", "Delivery": "14/03/2026", "Redelivery": "17/03/2026", "Durasi": 3.35, "HSD_L": 8452, "Harga_HSD": 19555, "Sewa": 164354167, "HSD_Rp": 165278860, "PBBKB": 15936246},
    {"Bulan": "Apr 2026", "Urutan": 4, "Kapal": "TB. MEDELIN CITRA", "Delivery": "04/04/2026", "Redelivery": "07/04/2026", "Durasi": 2.55, "HSD_L": 8363, "Harga_HSD": 19825, "Sewa": 125052083, "HSD_Rp": 165796475, "PBBKB": 15994238},
    {"Bulan": "Apr 2026", "Urutan": 4, "Kapal": "TB. AQUA HARBOUR", "Delivery": "09/04/2026", "Redelivery": "12/04/2026", "Durasi": 3.15, "HSD_L": 8031, "Harga_HSD": 19825, "Sewa": 154554167, "HSD_Rp": 159214575, "PBBKB": 15359288},
    {"Bulan": "Mei 2026", "Urutan": 5, "Kapal": "TB. AQUA HARBOUR", "Delivery": "03/05/2026", "Redelivery": "06/05/2026", "Durasi": 3.32, "HSD_L": 8039, "Harga_HSD": 28195, "Sewa": 162720833, "HSD_Rp": 226659605, "PBBKB": 22103231},
    {"Bulan": "Mei 2026", "Urutan": 5, "Kapal": "TB. MEDELIN CITRA", "Delivery": "29/05/2026", "Redelivery": "01/06/2026", "Durasi": 3.35, "HSD_L": 8700, "Harga_HSD": 24415, "Sewa": 164150000, "HSD_Rp": 212410500, "PBBKB": 20632050},
    {"Bulan": "Jun 2026", "Urutan": 6, "Kapal": "TB. MEDELIN CITRA", "Delivery": "22/06/2026", "Redelivery": "24/06/2026", "Durasi": 1.29, "HSD_L": 7144, "Harga_HSD": 24415, "Sewa": 63291667, "HSD_Rp": 174420760, "PBBKB": 16941996},
    {"Bulan": "Jul 2026", "Urutan": 7, "Kapal": "TB. AQUA HARBOUR", "Delivery": "04/07/2026", "Redelivery": "07/07/2026", "Durasi": 2.73, "HSD_L": 7914, "Harga_HSD": 23245, "Sewa": 133933333, "HSD_Rp": 183960930, "PBBKB": 17842113},
    {"Bulan": "Jul 2026", "Urutan": 7, "Kapal": "TB. MEDELIN PARTNER", "Delivery": "08/07/2026", "Redelivery": "09/07/2026", "Durasi": 1.41, "HSD_L": 3660, "Harga_HSD": 23245, "Sewa": 69008333, "HSD_Rp": 85076700, "PBBKB": 8251470},
    {"Bulan": "Jul 2026", "Urutan": 7, "Kapal": "TB. MEDELIN PARTNER", "Delivery": "19/07/2026", "Redelivery": "21/07/2026", "Durasi": 1.66, "HSD_L": 3999, "Harga_HSD": 23245, "Sewa": 81258333, "HSD_Rp": 92956755, "PBBKB": 9015746},
    {"Bulan": "Agt 2026", "Urutan": 8, "Kapal": "TB. AQUA HARBOUR", "Delivery": "10/08/2026", "Redelivery": "13/08/2026", "Durasi": 2.14, "HSD_L": 7062, "Harga_HSD": 17080, "Sewa": 104737500, "HSD_Rp": 120618960, "PBBKB": 11567556},
    {"Bulan": "Agt 2026", "Urutan": 8, "Kapal": "TB. MEDELIN CITRA", "Delivery": "24/08/2026", "Redelivery": "26/08/2026", "Durasi": 1.59, "HSD_L": 7708, "Harga_HSD": 17080, "Sewa": 77991667, "HSD_Rp": 131652640, "PBBKB": 12625704},
    {"Bulan": "Sep 2026", "Urutan": 9, "Kapal": "TB. MEDELIN PARTNER", "Delivery": "08/09/2026", "Redelivery": "10/09/2026", "Durasi": 1.65, "HSD_L": 4238, "Harga_HSD": 17080, "Sewa": 80645833, "HSD_Rp": 72385040, "PBBKB": 6941844},
    {"Bulan": "Sep 2026", "Urutan": 9, "Kapal": "TB. AQUA HARBOUR", "Delivery": "20/09/2026", "Redelivery": "23/09/2026", "Durasi": 3.11, "HSD_L": 7381, "Harga_HSD": 17755, "Sewa": 152512500, "HSD_Rp": 131049655, "PBBKB": 12588296},
    {"Bulan": "Sep 2026", "Urutan": 9, "Kapal": "TB. MEDELIN PARTNER", "Delivery": "29/09/2026", "Redelivery": "01/10/2026", "Durasi": 1.65, "HSD_L": 4205, "Harga_HSD": 17755, "Sewa": 81054167, "HSD_Rp": 74659775, "PBBKB": 7171628},
    {"Bulan": "Okt 2026", "Urutan": 10, "Kapal": "TB. MEDELIN PARTNER", "Delivery": "23/10/2026", "Redelivery": "25/10/2026", "Durasi": 1.60, "HSD_L": 4050, "Harga_HSD": 17755, "Sewa": 78604167, "HSD_Rp": 71907750, "PBBKB": 6907275},
]

if "records" not in st.session_state:
    st.session_state.records = INITIAL_DATA.copy()

def fmt_rp(val):
    return f"Rp {val:,.0f}".replace(",", ".")

def fmt_miliar(val):
    return f"Rp {val/1e9:,.2f} M".replace(".", ",")

# ==============================================================================
# HEADER
# ==============================================================================
st.markdown("""
<div class="main-header">
    <h1>🚢 Dashboard Monitoring Utilisasi & Revenue ARMAKUNG 2026</h1>
    <p>Gugus CIP FT Prove ARMAKUNG | PT Nusantara Regas – PT PGN LNG Indonesia | Skema Zero CAPEX & PKS Amendemen No. 8 (Rp 49 Jt/hari)</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR: FILTER & SIMULATOR CALL REAL-TIME
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Pengaturan & Filter")

    basis_pajak = st.radio(
        "Basis Perhitungan Revenue:",
        options=["Tanpa Pajak (Sewa + HSD)", "Grand Total (Incl. PBBKB 10%)"],
        index=0,
        help="Basis Tanpa Pajak disarankan untuk Form Verifikasi Keuangan sesuai asas fairness."
    )
    include_tax = basis_pajak == "Grand Total (Incl. PBBKB 10%)"

    df_all = pd.DataFrame(st.session_state.records)
    df_all["Tanpa_Pajak"] = df_all["Sewa"] + df_all["HSD_Rp"]
    df_all["Grand_Total"] = df_all["Tanpa_Pajak"] + df_all["PBBKB"]
    df_all["Kategori"] = df_all["Durasi"].apply(lambda x: "Full Service (>2 Hari)" if x > 2.0 else "Berthing Only (≤2 Hari)")

    selected_vessels = st.multiselect(
        "Filter Armada Tugboat:",
        options=sorted(df_all["Kapal"].unique()),
        default=sorted(df_all["Kapal"].unique())
    )

    selected_cat = st.multiselect(
        "Filter Kategori Layanan:",
        options=["Full Service (>2 Hari)", "Berthing Only (≤2 Hari)"],
        default=["Full Service (>2 Hari)", "Berthing Only (≤2 Hari)"]
    )

    st.divider()
    st.subheader("➕ Simulator Call (Nov–Des 2026)")
    st.caption("Tambahkan simulasi pelayanan untuk demo real-time di hadapan Dewan Juri.")

    with st.form("sim_form"):
        sim_bulan = st.selectbox("Bulan", ["Nov 2026", "Des 2026"])
        sim_kapal = st.selectbox("Armada Tugboat", ["TB. AQUA HARBOUR", "TB. MEDELIN CITRA", "TB. MEDELIN PARTNER"])
        sim_durasi = st.number_input("Durasi (Hari)", min_value=1.0, max_value=5.0, value=3.0, step=0.1)
        sim_hsd_l = st.number_input("Konsumsi HSD (Liter)", min_value=2000, max_value=12000, value=7800, step=100)
        sim_harga_hsd = st.number_input("Harga HSD (Rp/Liter)", min_value=15000, max_value=35000, value=18000, step=250)
        submitted = st.form_submit_button("Tambah ke Dashboard", use_container_width=True)

        if submitted:
            sewa_val = round(sim_durasi * 49_000_000)
            hsd_val = round(sim_hsd_l * sim_harga_hsd)
            pbbkb_val = round(hsd_val * 0.10)
            urutan = 11 if sim_bulan == "Nov 2026" else 12
            st.session_state.records.append({
                "Bulan": sim_bulan,
                "Urutan": urutan,
                "Kapal": sim_kapal,
                "Delivery": f"Simulasi ({sim_bulan})",
                "Redelivery": "-",
                "Durasi": sim_durasi,
                "HSD_L": sim_hsd_l,
                "Harga_HSD": sim_harga_hsd,
                "Sewa": sewa_val,
                "HSD_Rp": hsd_val,
                "PBBKB": pbbkb_val
            })
            st.rerun()

    if len(st.session_state.records) > len(INITIAL_DATA):
        if st.button("🔄 Reset ke Data Aktual (19 Call)", use_container_width=True):
            st.session_state.records = INITIAL_DATA.copy()
            st.rerun()

# ==============================================================================
# KALKULASI KPI DINAMIS
# ==============================================================================
df = df_all[
    (df_all["Kapal"].isin(selected_vessels)) &
    (df_all["Kategori"].isin(selected_cat))
].copy()

rev_col = "Grand_Total" if include_tax else "Tanpa_Pajak"
active_months = max(10, int(df_all["Urutan"].max()))  # 10 bln default, 11/12 jika ada simulasi
prorata_factor = 12 / active_months

total_rev = df[rev_col].sum()
proj_rev = total_rev * prorata_factor
total_calls = len(df)
annualized_calls = total_calls * prorata_factor

full_df = df[df["Durasi"] > 2.0]
avg_full_rev = full_df[rev_col].mean() if len(full_df) > 0 else 0
potensi_rev = avg_full_rev * annualized_calls if avg_full_rev > 0 else proj_rev
upside_pct = ((potensi_rev - proj_rev) / proj_rev * 100) if proj_rev > 0 else 0

total_durasi_hari = df["Durasi"].sum()
total_jam_pli = total_durasi_hari * 24

# ==============================================================================
# KPI CARDS
# ==============================================================================
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    label=f"Realisasi YTD ({active_months} Bln)",
    value=fmt_miliar(total_rev),
    delta=f"{total_calls} Call Aktual | {fmt_rp(total_rev)}"
)
c2.metric(
    label=f"Proyeksi FY 2026 (12/{active_months})",
    value=fmt_miliar(proj_rev),
    delta=f"Prorata {annualized_calls:.1f} Call/Tahun"
)
c3.metric(
    label="Potensi Full Service 2026",
    value=fmt_miliar(potensi_rev),
    delta=f"+{upside_pct:.1f}% vs Proyeksi"
)
c4.metric(
    label="Utilisasi Pelayanan PLI",
    value=f"{total_jam_pli:,.1f} Jam",
    delta=f"{total_durasi_hari:.2f} Hari | Zero CAPEX"
)

# ==============================================================================
# TABS KONTEN UTAMA
# ==============================================================================
tab1, tab2, tab3 = st.tabs([
    "📊 Analisis Revenue & Armada",
    "📋 Breakdown Transaksi & Ekspor",
    "🎯 Utilisasi & Benchmarking (SOFI)"
])

with tab1:
    # 1. Stacked Bar Chart Bulanan
    monthly = df.groupby(["Urutan", "Bulan"], as_index=False).agg(
        Calls=("Kapal", "count"),
        Sewa=("Sewa", "sum"),
        HSD_Rp=("HSD_Rp", "sum"),
        PBBKB=("PBBKB", "sum"),
        Total=(rev_col, "sum")
    ).sort_values("Urutan")

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=monthly["Bulan"], y=monthly["Sewa"], name="Biaya Sewa Kapal",
        marker_color="#1B365D", hovertemplate="Sewa: Rp %{y:,.0f}<extra></extra>"
    ))
    fig_bar.add_trace(go.Bar(
        x=monthly["Bulan"], y=monthly["HSD_Rp"], name="Biaya BBM (HSD)",
        marker_color="#3182CE", hovertemplate="HSD: Rp %{y:,.0f}<extra></extra>"
    ))
    if include_tax:
        fig_bar.add_trace(go.Bar(
            x=monthly["Bulan"], y=monthly["PBBKB"], name="Pajak PBBKB 10%",
            marker_color="#90CDF4", hovertemplate="PBBKB: Rp %{y:,.0f}<extra></extra>"
        ))

    fig_bar.update_layout(
        barmode="stack",
        title=f"Tren Pendapatan Bulanan 2026 — {basis_pajak}",
        xaxis_title="Bulan",
        yaxis_title="Rupiah (Rp)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 2. Dua Grafik Berdampingan: Per Armada & Per Kategori
    col_l, col_r = st.columns(2)
    with col_l:
        vessel_agg = df.groupby("Kapal", as_index=False).agg(
            Calls=("Bulan", "count"),
            Revenue=(rev_col, "sum"),
            Durasi=("Durasi", "sum")
        )
        fig_donut = px.pie(
            vessel_agg, values="Revenue", names="Kapal", hole=0.45,
            title="Kontribusi Pendapatan per Armada Tugboat",
            color_discrete_sequence=["#1B365D", "#2B6CB0", "#63B3ED"]
        )
        fig_donut.update_traces(textposition="inside", textinfo="percent+label")
        fig_donut.update_layout(height=360, showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_r:
        cat_agg = df.groupby("Kategori", as_index=False).agg(
            Calls=("Bulan", "count"),
            Rata_Rata=(rev_col, "mean"),
            Total=(rev_col, "sum")
        )
        fig_cat = px.bar(
            cat_agg, x="Kategori", y="Rata_Rata", text="Calls",
            color="Kategori",
            color_discrete_map={
                "Full Service (>2 Hari)": "#137333",
                "Berthing Only (≤2 Hari)": "#D97706"
            },
            title="Rata-rata Pendapatan per Call: Full Service vs Berthing Only"
        )
        fig_cat.update_traces(texttemplate="%{text} Call", textposition="outside")
        fig_cat.update_layout(height=360, showlegend=False, yaxis_title="Rata-rata Revenue (Rp)")
        st.plotly_chart(fig_cat, use_container_width=True)

with tab2:
    st.subheader("Rincian Transaksi Pelayanan Tugboat 2026")
    display_cols = ["Bulan", "Kapal", "Delivery", "Redelivery", "Durasi", "Kategori", "HSD_L", "Sewa", "HSD_Rp", "Tanpa_Pajak", "PBBKB", "Grand_Total"]
    st.dataframe(
        df[display_cols].style.format({
            "Durasi": "{:.2f} hr",
            "HSD_L": "{:,.0f} L",
            "Sewa": "Rp {:,.0f}",
            "HSD_Rp": "Rp {:,.0f}",
            "Tanpa_Pajak": "Rp {:,.0f}",
            "PBBKB": "Rp {:,.0f}",
            "Grand_Total": "Rp {:,.0f}"
        }),
        use_container_width=True,
        height=420
    )

    if len(df) > 0:
        s1, s2, s3 = st.columns(3)
        s1.info(f"**Rata-rata / Call:** {fmt_rp(df[rev_col].mean())}")
        max_row = df.loc[df[rev_col].idxmax()]
        min_row = df.loc[df[rev_col].idxmin()]
        s2.success(f"**Tertinggi (Max):** {fmt_rp(max_row[rev_col])} ({max_row['Kapal']} — {max_row['Bulan']})")
        s3.warning(f"**Terendah (Min):** {fmt_rp(min_row[rev_col])} ({min_row['Kapal']} — {min_row['Bulan']})")

    csv_data = df[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Unduh Data Rekap (CSV)",
        data=csv_data,
        file_name="Rekap_Pelayanan_ARMAKUNG_2026.csv",
        mime="text/csv"
    )

    st.caption(
        "Catatan Audit Asas Fairness: Transaksi TB. Medelin Citra periode 23–26 Desember 2025 "
        "(Rp 312.258.258 tanpa pajak / Rp 330.268.504 grand total dengan tarif lama Rp 38,295 Jt/hari) "
        "secara sengaja dikecualikan agar perhitungan murni berbasis 1 tahun anggaran 2026."
    )

with tab3:
    st.subheader("Benchmarking Industri & Roadmap Replikasi (Tindak Lanjut Form SOFI)")
    b1, b2 = st.columns(2)

    with b1:
        st.markdown("#### ⚓ Perbandingan Tarif & Praktik Terbaik Industri")
        bench_df = pd.DataFrame([
            {"Benchmark": "ARMAKUNG (NR – PLI)", "Skema": "Resource Sharing (On-Call)", "Biaya / Call": "Rp 263,9 Jt (Rata-rata Net)", "Lead Time": "Cepat (Standby Teluk Jakarta)"},
            {"Benchmark": "Spot Market Eksternal (JAI)", "Skema": "Sewa Pihak Ketiga", "Biaya / Call": "Hingga Rp 600 Jt / Call", "Lead Time": "Lebih lambat +52,13 Jam"},
            {"Benchmark": "PSA Marine Singapore", "Skema": "Shared Fleet & Pooling", "Biaya / Call": "Efisiensi Idle Cost", "Lead Time": "Real-time Dispatch"},
            {"Benchmark": "SIGTTO LNG Guidelines", "Skema": "Standar Keselamatan STS", "Biaya / Call": "Min. 11.000 HP (PM 57/2015)", "Lead Time": "Zero Incident Mandate"},
        ])
        st.table(bench_df)

    with b2:
        st.markdown("#### 🗺️ Roadmap Replikasi Pertamina Group")
        st.success("**Jangka Pendek (Subholding Gas):** Replikasi skema PKS two-way resource sharing ke Terminal Regasifikasi Arun (PAG) dan FSRU Jawa Satu.")
        st.info("**Jangka Menengah (Lintas Subholding):** Integrasi monetisasi idle time armada tunda bersama PT Pertamina Trans Kontinental (PTK) dan PT Pertamina International Shipping (PIS) di koridor Selat Sunda, Teluk Jakarta, dan Balikpapan.")
        st.warning("**Tata Kelola Keberlanjutan:** Gate Review kuartalan (HSSE & PSA), surveilans sertifikasi BKI (min. 11.000 HP), dan Annual Tariff Review PKS hingga 2027+.")