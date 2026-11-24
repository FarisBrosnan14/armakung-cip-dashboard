import os
import re
import io
import math
import base64
from datetime import date, datetime, timedelta
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

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
# CUSTOM CSS: DYNAMIC SLOW GRADIENT + LIVING ANIMATIONS + MID + STS CARDS
# ==============================================================================
st.markdown("""
<style>
@keyframes auroraBg {
    0%   { background-position: 0% 50%; }
    25%  { background-position: 50% 100%; }
    50%  { background-position: 100% 50%; }
    75%  { background-position: 50% 0%; }
    100% { background-position: 0% 50%; }
}
@keyframes titleGradientFlow {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes cardGradientDrift {
    0%   { background-position: 0% 0%; }
    50%  { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}
@keyframes scanLine {
    0%   { left: -38%; opacity: 0; }
    15%  { opacity: 1; }
    85%  { opacity: 1; }
    100% { left: 108%; opacity: 0; }
}
@keyframes amberGlow {
    0%, 100% { text-shadow: 0 0 10px rgba(255, 123, 58, 0.45); }
    50%      { text-shadow: 0 0 22px rgba(255, 145, 77, 0.92), 0 0 34px rgba(255, 123, 58, 0.40); }
}
@keyframes borderBreath {
    0%, 100% {
        border-color: rgba(0, 229, 255, 0.42);
        box-shadow: inset 0 0 14px rgba(0, 229, 255, 0.08), 0 0 12px rgba(0, 229, 255, 0.14);
    }
    50% {
        border-color: rgba(56, 232, 255, 0.82);
        box-shadow: inset 0 0 24px rgba(0, 229, 255, 0.20), 0 0 24px rgba(0, 229, 255, 0.30);
    }
}
@keyframes statusPulse {
    0%, 100% { transform: scale(1); }
    50%      { transform: scale(1.006); }
}
@keyframes liveDot {
    0%, 100% { opacity: 1; box-shadow: 0 0 8px #10b981; }
    50%      { opacity: 0.35; box-shadow: 0 0 2px #10b981; }
}

.stApp {
    background: linear-gradient(
        135deg,
        #030914 0%,
        #091c38 22%,
        #0f2d56 45%,
        #072540 68%,
        #0c1b36 85%,
        #040b18 100%
    );
    background-size: 320% 320%;
    animation: auroraBg 22s ease-in-out infinite;
    color: #e2e8f0;
    -webkit-tap-highlight-color: transparent;
}
header[data-testid="stHeader"] {
    background: rgba(5, 13, 26, 0.68);
    backdrop-filter: blur(8px);
}
.block-container {
    padding-top: 3.6rem !important;
    padding-bottom: 1.5rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
    max-width: 100%;
}

.cmd-title-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
    text-align: center;
    padding: 0.6rem 0.8rem 1rem 0.8rem;
    border-bottom: 1.5px solid rgba(0, 229, 255, 0.35);
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    background: linear-gradient(90deg, rgba(0,229,255,0.03), rgba(56,189,248,0.10), rgba(0,229,255,0.03));
    background-size: 250% 100%;
    animation: titleGradientFlow 14s ease-in-out infinite;
    border-radius: 10px 10px 0 0;
}
.cmd-title-wrap::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: -38%;
    width: 38%;
    height: 2.5px;
    background: linear-gradient(90deg, transparent, #00e5ff, #ffffff, #38bdf8, transparent);
    box-shadow: 0 0 14px #00e5ff;
    animation: scanLine 4.8s ease-in-out infinite;
}
.cmd-logo-box {
    background: rgba(255, 255, 255, 0.95);
    padding: 6px 12px;
    border-radius: 8px;
    border: 1.5px solid rgba(0, 229, 255, 0.80);
    box-shadow: 0 0 16px rgba(0, 229, 255, 0.38);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.28s ease, box-shadow 0.28s ease;
}
.cmd-logo-box:hover {
    transform: scale(1.06) rotate(-1deg);
    box-shadow: 0 0 26px rgba(0, 229, 255, 0.72);
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
    letter-spacing: 1.8px;
    background: linear-gradient(90deg, #38e8ff, #ffffff, #60a5fa, #00e5ff, #7dd3fc);
    background-size: 260% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: titleGradientFlow 8s ease-in-out infinite;
    filter: drop-shadow(0 0 12px rgba(0, 229, 255, 0.45));
    margin: 0;
    line-height: 1.25;
}
.cmd-subtitle {
    font-size: clamp(0.66rem, 0.95vw, 0.82rem);
    color: #94a3b8;
    letter-spacing: 1.4px;
    margin-top: 4px;
}

.kpi-box {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        125deg,
        rgba(10, 32, 64, 0.90),
        rgba(18, 52, 96, 0.86),
        rgba(7, 22, 46, 0.94),
        rgba(12, 42, 78, 0.88)
    );
    background-size: 260% 260%;
    border: 1px solid rgba(0, 229, 255, 0.50);
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.75rem;
    cursor: pointer;
    animation: cardGradientDrift 14s ease-in-out infinite, borderBreath 5s ease-in-out infinite;
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
    background: linear-gradient(115deg, transparent 20%, rgba(0, 229, 255, 0.28) 50%, transparent 80%);
    transition: left 0.65s ease;
    pointer-events: none;
}
.kpi-box:hover, .kpi-box:active {
    transform: translateY(-5px) scale(1.018);
    border-color: #00e5ff;
    box-shadow: inset 0 0 26px rgba(0, 229, 255, 0.28), 0 10px 28px rgba(0, 229, 255, 0.38);
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
    font-size: clamp(1.35rem, 1.9vw, 1.85rem);
    font-weight: 800;
    color: #ff7b3a;
    animation: amberGlow 3.2s ease-in-out infinite;
}
.kpi-unit {
    font-size: clamp(0.72rem, 0.85vw, 0.82rem);
    color: #7dd3fc;
    font-weight: 600;
}

.info-card {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(8, 22, 44, 0.84), rgba(14, 38, 72, 0.80), rgba(6, 18, 38, 0.88));
    background-size: 240% 240%;
    animation: cardGradientDrift 18s ease-in-out infinite;
    border: 1px solid rgba(0, 229, 255, 0.34);
    border-radius: 8px;
    padding: 11px 12px;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}
.info-card:hover, .info-card:active {
    transform: translateY(-3px);
    border-color: #00e5ff;
    box-shadow: 0 6px 22px rgba(0, 229, 255, 0.30);
}
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5.5px 4px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 4px;
    transition: background 0.2s ease, padding-left 0.2s ease;
}
.info-row:hover, .info-row:active {
    background: rgba(0, 229, 255, 0.12);
    padding-left: 8px;
}
.info-row:last-child { border-bottom: none; }

/* Multi-Information Display (MID) Operasional */
.mid-box {
    background: linear-gradient(145deg, rgba(7, 20, 42, 0.88), rgba(14, 38, 74, 0.82), rgba(5, 16, 34, 0.92));
    background-size: 240% 240%;
    animation: cardGradientDrift 16s ease-in-out infinite;
    border: 1px solid rgba(0, 229, 255, 0.40);
    border-radius: 8px;
    padding: 11px 12px;
    min-height: 224px;
}
.mid-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 12px;
    background: rgba(16, 185, 129, 0.16);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.45);
}
.live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10b981;
    display: inline-block;
    animation: liveDot 1.8s ease-in-out infinite;
}
.mid-highlight {
    background: rgba(0, 229, 255, 0.09);
    border: 1px solid rgba(0, 229, 255, 0.30);
    border-radius: 6px;
    padding: 8px 10px;
    margin: 7px 0;
}
.mid-bar-bg {
    width: 100%;
    height: 7px;
    background: rgba(255, 255, 255, 0.10);
    border-radius: 4px;
    overflow: hidden;
    margin-top: 4px;
}
.mid-bar-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #00e5ff, #38bdf8, #10b981);
}

.panel-header {
    background: linear-gradient(90deg, rgba(0, 229, 255, 0.24), rgba(56, 189, 248, 0.08), transparent);
    background-size: 220% 100%;
    animation: titleGradientFlow 12s ease-in-out infinite;
    border-left: 3px solid #00e5ff;
    padding: 6px 10px;
    font-size: clamp(0.82rem, 1vw, 0.94rem);
    font-weight: 700;
    color: #67e8f9;
    letter-spacing: 0.4px;
    margin-bottom: 8px;
    margin-top: 6px;
    border-radius: 0 5px 5px 0;
    transition: border-left-width 0.2s ease, color 0.2s ease, box-shadow 0.25s ease;
}
.panel-header:hover {
    border-left-width: 6px;
    color: #ffffff;
    box-shadow: inset 0 0 12px rgba(0, 229, 255, 0.18);
}

.sts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(225px, 1fr));
    gap: 10px;
    margin-top: 8px;
    margin-bottom: 10px;
}
.sts-card {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(10, 28, 56, 0.88), rgba(16, 46, 84, 0.80));
    border: 1px solid rgba(0, 229, 255, 0.35);
    border-radius: 8px;
    padding: 10px 12px;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}
.sts-card:hover {
    transform: translateY(-3px);
    border-color: #00e5ff;
    box-shadow: 0 6px 20px rgba(0, 229, 255, 0.28);
}
.sts-card.sts-conflict {
    border-color: #ef4444;
    background: linear-gradient(135deg, rgba(127, 29, 29, 0.42), rgba(30, 20, 36, 0.88));
    box-shadow: 0 0 16px rgba(239, 68, 68, 0.32);
}
.sts-card.sts-partial {
    border-color: #f59e0b;
    background: linear-gradient(135deg, rgba(120, 53, 15, 0.40), rgba(20, 30, 52, 0.88));
    box-shadow: 0 0 16px rgba(245, 158, 11, 0.28);
}
.sts-badge-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
}
.sts-date-pill {
    background: rgba(0, 229, 255, 0.18);
    color: #67e8f9;
    border: 1px solid rgba(0, 229, 255, 0.45);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.74rem;
    font-weight: 700;
}
.sts-tag {
    font-size: 0.70rem;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 10px;
}
.sts-tag-upcoming { background: rgba(56, 189, 248, 0.18); color: #7dd3fc; }
.sts-tag-active   { background: rgba(255, 123, 58, 0.25); color: #fdba74; }
.sts-tag-done     { background: rgba(148, 163, 184, 0.18); color: #94a3b8; }
.sts-vessel {
    font-size: 0.90rem;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 2px;
}
.sts-window {
    font-size: 0.76rem;
    color: #94a3b8;
}

.status-card {
    border-radius: 9px;
    padding: 15px 18px;
    margin-top: 10px;
    margin-bottom: 12px;
    font-size: 0.92rem;
    line-height: 1.55;
    animation: statusPulse 4s ease-in-out infinite;
}
.status-safe {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(6, 78, 59, 0.28));
    border: 1.5px solid #10b981;
    color: #d1fae5;
    box-shadow: 0 0 20px rgba(16, 185, 129, 0.24);
}
.status-warn {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.20), rgba(120, 53, 15, 0.30));
    border: 1.5px solid #f59e0b;
    color: #fef3c7;
    box-shadow: 0 0 20px rgba(245, 158, 11, 0.28);
}
.status-danger {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.22), rgba(127, 29, 29, 0.34));
    border: 1.5px solid #ef4444;
    color: #fee2e2;
    box-shadow: 0 0 22px rgba(239, 68, 68, 0.34);
}

div[data-testid="stPlotlyChart"] {
    border: 1px solid rgba(0, 229, 255, 0.24);
    border-radius: 8px;
    overflow: hidden;
    transition: border-color 0.28s ease, box-shadow 0.28s ease, transform 0.25s ease;
}
div[data-testid="stPlotlyChart"]:hover {
    border-color: rgba(0, 229, 255, 0.82);
    box-shadow: 0 0 22px rgba(0, 229, 255, 0.30);
    transform: translateY(-2px);
}

.stButton > button, .stDownloadButton > button {
    border: 1px solid rgba(0, 229, 255, 0.55) !important;
    transition: transform 0.18s ease, box-shadow 0.25s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    box-shadow: 0 0 16px rgba(0, 229, 255, 0.50) !important;
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
# HELPER PARSER PDF CARGO SCHEDULE (FORMAT NUSANTARA REGAS) & CEK BENTROK 3 LEVEL
# ==============================================================================
MONTH_MAP_ID_EN = {
    "jan": 1, "januari": 1, "january": 1,
    "feb": 2, "februari": 2, "february": 2,
    "mar": 3, "maret": 3, "march": 3,
    "apr": 4, "april": 4,
    "mei": 5, "may": 5,
    "jun": 6, "juni": 6, "june": 6,
    "jul": 7, "juli": 7, "july": 7,
    "agt": 8, "agu": 8, "agustus": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "des": 12, "desember": 12, "dec": 12, "december": 12,
}

def extract_sts_from_pdf(uploaded_file, default_year=2026, default_sts_days=3):
    """Membaca jadwal Cargo STS dari PDF PT Nusantara Regas (kolom ETA DD-Mon) maupun format standar."""
    if not HAS_PDFPLUMBER:
        return [], "Library `pdfplumber` belum terpasang. Pastikan `pdfplumber>=0.10.0` ada di requirements.txt."

    extracted = []
    seen_keys = set()
    raw_text_all = ""
    sts_span = max(0, int(default_sts_days) - 1)

    eta_dd_mon_pat = re.compile(r'\b(\d{1,2})[-/\s]([A-Za-z]{3,9})\b')
    cargo_no_pat = re.compile(r'\b([A-Z]{2}\d{2,3})\b')

    try:
        with pdfplumber.open(io.BytesIO(uploaded_file.getvalue())) as pdf:
            for page_idx, page in enumerate(pdf.pages, start=1):
                txt = page.extract_text() or ""
                raw_text_all += f"\n--- Page {page_idx} ---\n" + txt

                yr_match = re.search(r'\b(202\d|203\d)\b', txt)
                doc_year = int(yr_match.group(1)) if yr_match else int(default_year)

                tables = page.extract_tables() or []
                for tbl in tables:
                    if not tbl or len(tbl) < 2:
                        continue
                    eta_col, lngc_col, cargo_col = None, None, None
                    for row in tbl[:5]:
                        for c_idx, cell in enumerate(row):
                            s = str(cell or "").strip().upper()
                            if s in ("ETA", "ΕΤΑ") or "ETA" in s:
                                eta_col = c_idx
                            elif "LNGC" in s or "VESSEL" in s:
                                lngc_col = c_idx
                            elif "CARGO" in s:
                                cargo_col = c_idx

                    for row in tbl:
                        if not row:
                            continue
                        row_str = " ".join(str(c or "") for c in row)
                        low_row = row_str.lower()
                        if "based on mom" in low_row or "delivery status" in low_row:
                            continue

                        cand_cols = [eta_col] if eta_col is not None and eta_col < len(row) else list(range(min(7, len(row))))
                        for c_idx in cand_cols:
                            cell_val = str(row[c_idx] or "").strip()
                            m = eta_dd_mon_pat.search(cell_val)
                            if m:
                                d_str, mon_str = m.groups()
                                mon_num = MONTH_MAP_ID_EN.get(mon_str.lower())
                                if not mon_num:
                                    continue
                                d_num = int(d_str)
                                if not (1 <= d_num <= 31):
                                    continue
                                try:
                                    dt_start = date(doc_year, mon_num, d_num)
                                    dt_end = dt_start + timedelta(days=sts_span)
                                except ValueError:
                                    continue

                                vessel = ""
                                if lngc_col is not None and lngc_col < len(row):
                                    vessel = " ".join(str(row[lngc_col] or "").split())
                                c_no = ""
                                if cargo_col is not None and cargo_col < len(row):
                                    c_no = " ".join(str(row[cargo_col] or "").split())
                                if not c_no:
                                    cm = cargo_no_pat.search(row_str)
                                    c_no = cm.group(1) if cm else ""

                                parts = ["STS"]
                                if vessel and vessel.upper() != "LNGC":
                                    parts.append(vessel)
                                if c_no and "CARGO" not in c_no.upper():
                                    parts.append(f"({c_no})")
                                ket = " ".join(parts) if len(parts) > 1 else f"STS FSRU NR (Hal. {page_idx})"

                                key = (dt_start, dt_end, c_no)
                                if key not in seen_keys:
                                    seen_keys.add(key)
                                    extracted.append({
                                        "Tanggal_Mulai": dt_start,
                                        "Tanggal_Selesai": dt_end,
                                        "Keterangan": ket,
                                        "Sumber": uploaded_file.name
                                    })
                                break

                for raw_line in txt.splitlines():
                    line = " ".join(raw_line.split())
                    if not line:
                        continue
                    low = line.lower()
                    if any(skip in low for skip in ["based on mom", "delivery status", "cargo schedule", "created by", "note:"]):
                        continue

                    for m in eta_dd_mon_pat.finditer(line):
                        d_str, mon_str = m.groups()
                        mon_num = MONTH_MAP_ID_EN.get(mon_str.lower())
                        if not mon_num:
                            continue
                        d_num = int(d_str)
                        if not (1 <= d_num <= 31):
                            continue
                        try:
                            dt_start = date(doc_year, mon_num, d_num)
                            dt_end = dt_start + timedelta(days=sts_span)
                        except ValueError:
                            continue

                        cm = cargo_no_pat.search(line)
                        c_no = cm.group(1) if cm else ""
                        vm = re.match(r'^\d+\s+([A-Za-z0-9\.\-\s]+?)\s+(?:Tangguh|Bontang|Donggi|Badak|PLN|PG|DES|FOB)', line, re.IGNORECASE)
                        vessel = vm.group(1).strip() if vm else ""

                        if any(k[0] == dt_start and (k[2] == c_no or not c_no) for k in seen_keys):
                            continue

                        parts = ["STS"]
                        if vessel:
                            parts.append(vessel)
                        if c_no:
                            parts.append(f"({c_no})")
                        ket = " ".join(parts) if len(parts) > 1 else f"STS FSRU NR (Hal. {page_idx})"

                        seen_keys.add((dt_start, dt_end, c_no))
                        extracted.append({
                            "Tanggal_Mulai": dt_start,
                            "Tanggal_Selesai": dt_end,
                            "Keterangan": ket,
                            "Sumber": uploaded_file.name
                        })
    except Exception as e:
        return [], f"Gagal memindai PDF: {e}"

    extracted.sort(key=lambda x: x["Tanggal_Mulai"])
    return extracted, raw_text_all


def check_sts_availability(req_start: date, durasi_hari: float, sts_df: pd.DataFrame):
    """
    Logika 3 Keputusan Operasional untuk Input 1 (Pre-Check Ajuan):
    - Input hanya: Tanggal Mulai Ajuan + Durasi (Hari).
    - Output:
      1) 'BISA'          : Tidak ada irisan hari dengan jadwal STS FSRU NR -> Full Service.
      2) 'BERTHING_ONLY' : Hari mulai aman, namun hari lanjutan beririsan STS NR -> Hanya Assist Berthing Saja.
      3) 'TIDAK_BISA'    : Tanggal mulai jatuh tepat pada hari STS FSRU NR -> Tidak Bisa Sama Sekali.
    """
    span_days = max(1, int(math.ceil(durasi_hari)))
    req_end = req_start + timedelta(days=span_days - 1)
    req_days = {req_start + timedelta(days=i) for i in range(span_days)}

    if sts_df is None or sts_df.empty:
        return "BISA", req_end, [], set()

    conflicts = []
    overlap_days_all = set()
    start_blocked = False

    for _, row in sts_df.iterrows():
        s_start = pd.to_datetime(row["Tanggal_Mulai"]).date()
        s_end = pd.to_datetime(row["Tanggal_Selesai"]).date()
        sts_days = {s_start + timedelta(days=i) for i in range((s_end - s_start).days + 1)}
        inter = req_days.intersection(sts_days)
        if inter:
            overlap_days_all.update(inter)
            if req_start in sts_days:
                start_blocked = True
            conflicts.append({
                "STS_Mulai": s_start,
                "STS_Selesai": s_end,
                "Keterangan": row.get("Keterangan", "STS FSRU NR"),
                "Hari_Irisan": sorted(inter)
            })

    if not conflicts:
        return "BISA", req_end, [], set()
    if start_blocked:
        return "TIDAK_BISA", req_end, conflicts, overlap_days_all
    return "BERTHING_ONLY", req_end, conflicts, overlap_days_all


# ==============================================================================
# DATA AKTUAL 2026 (JAN–OKT 2026, 19 CALL) & JADWAL CARGO STS NOV–DES 2026
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

INITIAL_STS_SCHEDULE = [
    {"Tanggal_Mulai": date(2026, 11, 6),  "Tanggal_Selesai": date(2026, 11, 8),  "Keterangan": "STS Prima Concord (LN42)", "Sumber": "Cargo Schedule Nov-Dec 2026"},
    {"Tanggal_Mulai": date(2026, 11, 13), "Tanggal_Selesai": date(2026, 11, 15), "Keterangan": "STS SC Serenity (LN43)",   "Sumber": "Cargo Schedule Nov-Dec 2026"},
    {"Tanggal_Mulai": date(2026, 11, 20), "Tanggal_Selesai": date(2026, 11, 22), "Keterangan": "STS Golden Quina (LS17)",  "Sumber": "Cargo Schedule Nov-Dec 2026"},
    {"Tanggal_Mulai": date(2026, 11, 27), "Tanggal_Selesai": date(2026, 11, 29), "Keterangan": "STS SC Serenity (LN44)",   "Sumber": "Cargo Schedule Nov-Dec 2026"},
    {"Tanggal_Mulai": date(2026, 12, 4),  "Tanggal_Selesai": date(2026, 12, 6),  "Keterangan": "STS Prima Carrier (LS19)", "Sumber": "Cargo Schedule Nov-Dec 2026"},
    {"Tanggal_Mulai": date(2026, 12, 12), "Tanggal_Selesai": date(2026, 12, 14), "Keterangan": "STS Golden Isaia (LJ16)",  "Sumber": "Cargo Schedule Nov-Dec 2026"},
    {"Tanggal_Mulai": date(2026, 12, 19), "Tanggal_Selesai": date(2026, 12, 21), "Keterangan": "STS SC Serenity (LN45)",   "Sumber": "Cargo Schedule Nov-Dec 2026"},
    {"Tanggal_Mulai": date(2026, 12, 27), "Tanggal_Selesai": date(2026, 12, 29), "Keterangan": "STS Prima Carrier (LN46)", "Sumber": "Cargo Schedule Nov-Dec 2026"},
]

if "df_data" not in st.session_state:
    st.session_state.df_data = pd.DataFrame(INITIAL_DATA)

if "df_sts" not in st.session_state:
    st.session_state.df_sts = pd.DataFrame(INITIAL_STS_SCHEDULE)

if "pdf_scan_history" not in st.session_state:
    st.session_state.pdf_scan_history = []

if "pdf_uploader_key" not in st.session_state:
    st.session_state.pdf_uploader_key = 0

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
    st.markdown("### 📂 Muat Data Rekap dari CSV")
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

st.markdown(
    f'<div class="cmd-title-wrap">{logo_html}'
    f'<div><div class="cmd-title">ARMAKUNG MARITIME MONITORING &amp; FUEL COMMAND CENTER</div>'
    f'<div class="cmd-subtitle">PT NUSANTARA REGAS</div></div></div>',
    unsafe_allow_html=True
)

# ==============================================================================
# BARIS 1: 3 KARTU KPI UTAMA
# ==============================================================================
k1, k2, k3 = st.columns(3)
with k1:
    st.markdown(
        f'<div class="kpi-box" tabindex="0">'
        f'<div class="kpi-label">Realisasi Revenue YTD ({active_months} Bulan)</div>'
        f'<div class="kpi-value-row">'
        f'<span class="kpi-val">{total_rev/1e9:,.2f} Miliar</span>'
        f'<span class="kpi-unit">IDR &bull; {total_calls} Call Aktual</span>'
        f'</div></div>',
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f'<div class="kpi-box" tabindex="0">'
        f'<div class="kpi-label">Proyeksi 1 Tahun Anggaran (12/{active_months})</div>'
        f'<div class="kpi-value-row">'
        f'<span class="kpi-val">{proj_rev/1e9:,.2f} Miliar</span>'
        f'<span class="kpi-unit">IDR &bull; {ann_calls:.1f} Call/Thn</span>'
        f'</div></div>',
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f'<div class="kpi-box" tabindex="0">'
        f'<div class="kpi-label">Potensi Full Service 2026</div>'
        f'<div class="kpi-value-row">'
        f'<span class="kpi-val">{potensi_rev/1e9:,.2f} Miliar</span>'
        f'<span class="kpi-unit">IDR &bull; Zero CAPEX</span>'
        f'</div></div>',
        unsafe_allow_html=True
    )

PLOT_BG = "rgba(8, 22, 44, 0.72)"
FONT_CLR = "#cbd5e1"
GRID_CLR = "rgba(0, 229, 255, 0.14)"

# ==============================================================================
# BARIS 2: 2 KOLOM OPTIMAL (TANPA KOMPOSISI REVENUE — PETA & INFO LEBIH LEGA)
# ==============================================================================
col_left, col_mid = st.columns([1.32, 2.68], gap="small")

with col_left:
    st.markdown('<div class="panel-header">⚓ Revenue per Armada (Miliar Rp)</div>', unsafe_allow_html=True)
    v_agg = df.groupby("Kapal", as_index=False).agg(Rev=(rev_col, "sum"), Calls=("Bulan", "count")).sort_values("Rev")
    max_v = (v_agg["Rev"].max() / 1e9) * 1.25 if len(v_agg) > 0 else 3
    fig_hbar = go.Figure(go.Bar(
        x=v_agg["Rev"] / 1e9,
        y=v_agg["Kapal"].str.replace("TB. ", ""),
        orientation="h",
        marker=dict(color=["#38bdf8", "#6366f1", "#00e5ff"][:len(v_agg)], line=dict(color="#00e5ff", width=1)),
        text=[f"Rp {r/1e9:.2f} M ({c}x)" for r, c in zip(v_agg["Rev"], v_agg["Calls"])],
        textposition="auto",
        textfont=dict(size=10.5, family="Segoe UI"),
        hovertemplate="<b>%{y}</b><br>Revenue: Rp %{x:.2f} M<extra></extra>"
    ))
    fig_hbar.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=FONT_CLR, size=10.5),
        height=230, margin=dict(l=8, r=18, t=12, b=28),
        xaxis=dict(gridcolor=GRID_CLR, title="Miliar Rp", range=[0, max_v], automargin=True),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", automargin=True)
    )
    st.plotly_chart(fig_hbar, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="panel-header">⏱️ Ringkasan Operasional &amp; Rekor Call 2026</div>', unsafe_allow_html=True)
    total_jam = df["Durasi"].sum() * 24
    total_hsd = df["HSD_L"].sum()
    if len(df) > 0:
        max_r = df.loc[df[rev_col].idxmax()]
        min_r = df.loc[df[rev_col].idxmin()]
        avg_v = df[rev_col].mean()
        rekor_html = (
            f'<div class="info-row"><span style="color:#94a3b8;">Tertinggi (Max &bull; {max_r["Bulan"]})</span>'
            f'<b style="color:#4ade80;">Rp {max_r[rev_col]:,.0f}</b></div>'
            f'<div class="info-row"><span style="color:#94a3b8;">Rata-rata per Call</span>'
            f'<b style="color:#00e5ff;">Rp {avg_v:,.0f}</b></div>'
            f'<div class="info-row"><span style="color:#94a3b8;">Terendah (Min &bull; {min_r["Bulan"]})</span>'
            f'<b style="color:#facc15;">Rp {min_r[rev_col]:,.0f}</b></div>'
        )
    else:
        rekor_html = ""

    st.markdown(
        f'<div class="info-card" style="font-size:0.84rem;" tabindex="0">'
        f'<div class="info-row"><span style="color:#94a3b8;">Total Durasi Layanan</span><b style="color:#00e5ff;">{df["Durasi"].sum():.2f} Hr ({total_jam:,.0f} Jam)</b></div>'
        f'<div class="info-row"><span style="color:#94a3b8;">Total Konsumsi HSD</span><b style="color:#ffeb3b;">{total_hsd:,.0f} Liter</b></div>'
        f'<div class="info-row"><span style="color:#94a3b8;">Full Service vs Partial</span><b style="color:#4ade80;">{len(full_df)} Full / {len(df)-len(full_df)} Partial</b></div>'
        f'<div class="info-row"><span style="color:#94a3b8;">Lead Time Saving</span><b style="color:#ff7b3a;">52,13 Jam (748% Lebih Cepat)</b></div>'
        f'{rekor_html}'
        f'</div>',
        unsafe_allow_html=True
    )

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
            #map { flex:1; width:100%; min-height:260px; background:#050d1a; }

            .dark-navy-tiles {
                filter: invert(100%) hue-rotate(190deg) brightness(86%) contrast(95%) saturate(135%);
            }

            @keyframes routeFlow {
                from { stroke-dashoffset: 44; }
                to   { stroke-dashoffset: 0; }
            }
            @keyframes panelGradient {
                0%   { background-position: 0% 50%; }
                50%  { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
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
                position: absolute; top: 10px; right: 10px; width: 270px;
                background: linear-gradient(135deg, rgba(10, 22, 42, 0.95), rgba(16, 40, 76, 0.92), rgba(8, 18, 36, 0.95));
                background-size: 220% 220%;
                animation: panelGradient 14s ease-in-out infinite;
                color: #fff; z-index: 9999;
                border: 1px solid rgba(0, 229, 255, 0.75); border-radius: 7px;
                box-shadow: 0 0 18px rgba(0, 229, 255, 0.30); backdrop-filter: blur(6px);
                overflow: hidden;
                transition: box-shadow 0.25s ease, border-color 0.25s ease;
            }
            .calc-panel:hover {
                border-color: #00e5ff;
                box-shadow: 0 0 26px rgba(0, 229, 255, 0.48);
            }
            .calc-hdr {
                background: linear-gradient(90deg, #0b2545, #184a88, #0b2545);
                background-size: 200% 100%;
                animation: panelGradient 10s ease-in-out infinite;
                padding: 7px 10px;
                display:flex; justify-content:space-between; align-items:center;
                border-bottom: 1.5px solid #00e5ff; cursor: pointer;
            }
            .calc-body { padding: 9px; font-size: 11px; }
            .cfg-box { background: rgba(0,229,255,0.08); border:1px solid rgba(0,229,255,0.35); border-radius:4px; padding:6px; margin-bottom:6px; }
            .row2 { display:flex; justify-content:space-between; gap:6px; margin-top:4px; }
            input, select {
                background:#061124; color:#fff; border:1px solid #334155; border-radius:3px;
                padding:3px 5px; font-size:11px; width:100%;
                transition: border-color 0.2s ease, box-shadow 0.2s ease;
            }
            input:focus, select:focus {
                outline: none; border-color: #00e5ff; box-shadow: 0 0 8px rgba(0,229,255,0.5);
            }
            .wx-box { background: rgba(0,0,0,0.35); border:1px solid #334155; border-radius:4px; padding:6px; margin-bottom:6px; }
            .wx-grid { display:flex; justify-content:space-between; text-align:center; margin-top:3px; }
            .btn-sm {
                border:none; border-radius:3px; padding:4px 6px; font-size:10px; font-weight:700; cursor:pointer;
                transition: transform 0.15s ease, filter 0.2s ease;
            }
            .btn-sm:hover { filter: brightness(1.15); transform: translateY(-1px); }
            .btn-sm:active { transform: scale(0.94); }
            table { width:100%; border-collapse:collapse; margin-top:6px; font-size:11px; }
            td { padding:3.5px 2px; border-bottom:1px solid rgba(255,255,255,0.09); }
            tr:hover td { background: rgba(0,229,255,0.08); }
            .val { text-align:right; font-weight:700; }

            @media (max-width: 600px) {
                html, body { overflow-y: auto; }
                .wrap { height: auto; }
                #map { height: 250px; flex: none; }
                .calc-panel { position: relative; top: 0; right: 0; width: 100%; margin-top: 6px; border-radius: 6px; }
            }
        </style>
    </head>
    <body>
        <div class="wrap">
            <div id="map"></div>
            <div class="calc-panel">
                <div class="calc-hdr" onclick="toggleCalc()">
                    <span style="color:#00e5ff; font-weight:800; font-size:11.5px;">⛽ NR FUEL &amp; CHARTER CALC</span>
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

                    <div class="row2" style="margin-bottom:4px;">
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
                            <td id="val_total" class="val" style="color:#ff7b3a; font-size:12px;">--</td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>

        <script>
            var map = L.map('map', { center: [-5.75, 106.45], zoom: 8, doubleClickZoom: false });

            var osmDark = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap', maxZoom: 19, className: 'dark-navy-tiles'
            }).addTo(map);

            var esriSat = L.layerGroup([
                L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                    attribution: 'Esri Satellite', maxZoom: 19
                }),
                L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
                    maxZoom: 19
                })
            ]);

            var esriOcean = L.layerGroup([
                L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}', {
                    attribution: 'Esri Ocean', maxZoom: 13
                }),
                L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Reference/MapServer/tile/{z}/{y}/{x}', {
                    maxZoom: 13
                })
            ]);

            var osmLight = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap', maxZoom: 19
            });

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
    components.html(map_html, height=530, scrolling=True)

# ==============================================================================
# BARIS 3: MULTI-INFORMATION DISPLAY (PENGGANTI PANCA MUTU) | TREN | AKUMULASI
# ==============================================================================
b1, b2, b3 = st.columns([1.25, 1.35, 1.15], gap="small")

with b1:
    st.markdown('<div class="panel-header">🛰️ Dispatch Intelligence (Multi-Info Display)</div>', unsafe_allow_html=True)
    mid_t1, mid_t2, mid_t3 = st.tabs(["⚡ Ready & STS", "⛽ Eco-Dispatch", "💰 Group Saving"])

    # --- MID TAB 1: LIVE DISPATCH WINDOW & NEXT STS COUNTDOWN ---
    with mid_t1:
        today_ref = date.today()
        sts_tmp = st.session_state.df_sts.copy()
        next_sts_html = '<div style="color:#94a3b8; font-size:0.82rem;">Belum ada jadwal STS mendatang.</div>'
        window_badge = '<span class="mid-badge"><span class="live-dot"></span> ARMADA STANDBY OPEN</span>'

        if not sts_tmp.empty:
            sts_tmp["Tanggal_Mulai"] = pd.to_datetime(sts_tmp["Tanggal_Mulai"]).dt.date
            sts_tmp["Tanggal_Selesai"] = pd.to_datetime(sts_tmp["Tanggal_Selesai"]).dt.date
            sts_tmp = sts_tmp.sort_values("Tanggal_Mulai")
            active_now = sts_tmp[(sts_tmp["Tanggal_Mulai"] <= today_ref) & (sts_tmp["Tanggal_Selesai"] >= today_ref)]
            upcoming = sts_tmp[sts_tmp["Tanggal_Mulai"] > today_ref]

            if not active_now.empty:
                cur = active_now.iloc[0]
                window_badge = '<span class="mid-badge" style="background:rgba(239,68,68,0.18);color:#fca5a5;border-color:#ef4444;">🔴 STS NR SEDANG BERLANGSUNG</span>'
                next_sts_html = (
                    f'<div class="mid-highlight">'
                    f'<div style="font-size:0.72rem; color:#fca5a5; font-weight:700;">LOCKED — OPERASI STS FSRU NR</div>'
                    f'<div style="font-size:0.92rem; font-weight:800; color:#fff;">🚢 {cur["Keterangan"]}</div>'
                    f'<div style="font-size:0.76rem; color:#cbd5e1;">Selesai: {cur["Tanggal_Selesai"].strftime("%d %b %Y")} (Standby Penuh)</div>'
                    f'</div>'
                )
            elif not upcoming.empty:
                nxt = upcoming.iloc[0]
                days_to_sts = (nxt["Tanggal_Mulai"] - today_ref).days
                safe_days = max(0, days_to_sts - 1)
                if safe_days >= 3:
                    win_txt = f'Bisa Full Service s/d {(nxt["Tanggal_Mulai"] - timedelta(days=1)).strftime("%d %b")}'
                    win_clr = "#34d399"
                elif safe_days >= 1:
                    win_txt = f'Window sempit ({safe_days} hr) — Disarankan Berthing Only'
                    win_clr = "#fbbf24"
                else:
                    win_txt = "H-1 STS NR — Armada Standby"
                    win_clr = "#f87171"
                next_sts_html = (
                    f'<div class="mid-highlight">'
                    f'<div style="display:flex; justify-content:space-between; font-size:0.72rem; color:#7dd3fc; font-weight:700;">'
                    f'<span>NEXT CARGO STS NR</span><span>H-{days_to_sts}</span></div>'
                    f'<div style="font-size:0.90rem; font-weight:800; color:#fff; margin-top:2px;">🚢 {nxt["Keterangan"]}</div>'
                    f'<div style="font-size:0.76rem; color:#cbd5e1;">ETA: {nxt["Tanggal_Mulai"].strftime("%d %b")} – {nxt["Tanggal_Selesai"].strftime("%d %b %Y")}</div>'
                    f'<div style="font-size:0.75rem; color:{win_clr}; font-weight:700; margin-top:4px;">⚡ {win_txt}</div>'
                    f'</div>'
                )

        st.markdown(
            f'<div class="mid-box" style="font-size:0.80rem;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">'
            f'{window_badge}<span style="font-size:0.72rem; color:#94a3b8;">PM 57/2015</span></div>'
            f'{next_sts_html}'
            f'<div class="info-row"><span style="color:#94a3b8;">Total Daya Armada</span><b style="color:#00e5ff;">12.000 HP (Min 11.000 HP)</b></div>'
            f'<div class="info-row"><span style="color:#94a3b8;">Bollard Pull / Safety</span><b style="color:#4ade80;">≥125 Ton &bull; Zero Accident</b></div>'
            f'</div>',
            unsafe_allow_html=True
        )

    # --- MID TAB 2: ECO-DISPATCH RANKING (REKOMENDASI KAPAL PALING HEMAT BBM) ---
    with mid_t2:
        if len(df) > 0:
            eco = df.groupby("Kapal", as_index=False).agg(
                Durasi=("Durasi", "sum"),
                HSD_L=("HSD_L", "sum"),
                Rev=(rev_col, "sum")
            )
            eco["L_per_Hari"] = eco["HSD_L"] / eco["Durasi"].replace(0, 1)
            eco = eco.sort_values("L_per_Hari").reset_index(drop=True)
            best_v = eco.iloc[0]
            avg_hsd_hrg = df["Harga_HSD"].mean()
            last_hsd_hrg = df.iloc[-1]["Harga_HSD"]
            hsd_diff_pct = ((last_hsd_hrg - avg_hsd_hrg) / avg_hsd_hrg * 100) if avg_hsd_hrg > 0 else 0
            hsd_clr = "#4ade80" if hsd_diff_pct <= 0 else "#f87171"

            eco_rows = []
            for idx_e, er in eco.iterrows():
                medal = "🥇" if idx_e == 0 else ("🥈" if idx_e == 1 else "🥉")
                eco_rows.append(
                    f'<div class="info-row">'
                    f'<span style="color:#e2e8f0;">{medal} {er["Kapal"].replace("TB. ","")}</span>'
                    f'<b style="color:#ffeb3b;">{er["L_per_Hari"]:,.0f} L/Hr</b>'
                    f'</div>'
                )
            st.markdown(
                f'<div class="mid-box" style="font-size:0.80rem;">'
                f'<div class="mid-highlight" style="margin-top:0;">'
                f'<div style="font-size:0.71rem; color:#4ade80; font-weight:700;">🌿 REKOMENDASI ECO-DISPATCH</div>'
                f'<div style="font-size:0.88rem; font-weight:800; color:#fff;">{best_v["Kapal"]} ({best_v["L_per_Hari"]:,.0f} L/hari)</div>'
                f'</div>'
                f'{"".join(eco_rows)}'
                f'<div class="info-row"><span style="color:#94a3b8;">Harga HSD Terakhir vs Avg</span>'
                f'<b style="color:{hsd_clr};">Rp {last_hsd_hrg:,.0f}/L ({hsd_diff_pct:+.1f}%)</b></div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.info("Pilih minimal 1 armada pada filter.")

    # --- MID TAB 3: SUNK COST RECOVERY & PERTAMINA GROUP SAVING ---
    with mid_t3:
        spot_benchmark_per_call = 600_000_000
        spot_total = spot_benchmark_per_call * total_calls
        group_saving = max(0, spot_total - total_rev)
        saving_pct = (group_saving / spot_total * 100) if spot_total > 0 else 0
        sewa_murni = df["Sewa"].sum()
        standby_days_recovered = sewa_murni / 31_800_000 if sewa_murni > 0 else 0

        st.markdown(
            f'<div class="mid-box" style="font-size:0.80rem;">'
            f'<div class="mid-highlight" style="margin-top:0;">'
            f'<div style="font-size:0.71rem; color:#7dd3fc; font-weight:700;">💎 PERTAMINA GROUP COST AVOIDANCE</div>'
            f'<div style="font-size:1.05rem; font-weight:800; color:#4ade80;">Rp {group_saving/1e9:,.2f} Miliar</div>'
            f'<div style="font-size:0.72rem; color:#cbd5e1;">Hemat {saving_pct:.1f}% vs Spot Market (Rp 600 Jt/call)</div>'
            f'<div class="mid-bar-bg"><div class="mid-bar-fill" style="width:{min(100, saving_pct):.0f}%;"></div></div>'
            f'</div>'
            f'<div class="info-row"><span style="color:#94a3b8;">Sewa Murni (Excl. HSD)</span><b style="color:#00e5ff;">Rp {sewa_murni/1e9:,.2f} M</b></div>'
            f'<div class="info-row"><span style="color:#94a3b8;">Sunk Cost Recovered</span><b style="color:#ff7b3a;">≈ {standby_days_recovered:.0f} Hari Standby</b></div>'
            f'</div>',
            unsafe_allow_html=True
        )

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
# BARIS 4: INPUT 1 — CEK BENTROK AJUAN & VISUALISASI JADWAL CARGO STS FSRU NR
# ==============================================================================
st.markdown('<div class="panel-header">📅 INPUT 1 — Cek Jadwal Bentrok Ajuan ARMAKUNG &amp; Kalender Cargo STS FSRU NR</div>', unsafe_allow_html=True)

tab_cek, tab_pdf, tab_sts_tbl = st.tabs([
    "🔍 Cek Bentrok & Timeline STS",
    "📄 Upload & Scan PDF Cargo Schedule",
    "🛠️ Edit Manual Jadwal STS"
])

with tab_cek:
    st.caption("Masukkan **Tanggal Mulai Ajuan** dan **Durasi (Hari)** dari permintaan peminjaman Tugboat. Sistem otomatis mengecek apakah operasi **Bisa Dilakukan (Full Service)**, **Hanya Assist Berthing Saja**, atau **Tidak Bisa Sama Sekali**.")

    in_c1, in_c2 = st.columns([1.2, 1.0])
    with in_c1:
        tgl_ajuan = st.date_input("Tanggal Mulai Ajuan (Delivery)", value=date(2026, 12, 3), key="cek_tgl_ajuan")
    with in_c2:
        durasi_ajuan = st.number_input("Durasi Ajuan (Hari)", min_value=1, max_value=10, value=3, step=1, key="cek_durasi_ajuan")

    status_code, tgl_selesai_ajuan, conflict_list, overlap_days = check_sts_availability(
        tgl_ajuan, durasi_ajuan, st.session_state.df_sts
    )
    lead_days = (tgl_ajuan - date.today()).days
    h5_note = f"✅ Memenuhi SLA Request H-5 ({lead_days} hari ke depan)" if lead_days >= 5 else f"⚠️ Kurang dari SLA H-5 ({lead_days} hari dari hari ini)"

    if status_code == "BISA":
        st.markdown(
            f'<div class="status-card status-safe">'
            f'<div style="font-size:1.05rem; font-weight:800;">✅ BISA DILAKUKAN — FULL SERVICE (BERTHING &amp; UNBERTHING)</div>'
            f'Periode ajuan <b>{tgl_ajuan.strftime("%d %b %Y")} s/d {tgl_selesai_ajuan.strftime("%d %b %Y")}</b> ({durasi_ajuan} hari) '
            f'<b>aman dan tidak beririsan</b> dengan jadwal Cargo STS FSRU NR.<br>'
            f'<span style="font-size:0.82rem; opacity:0.9;">{h5_note}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    elif status_code == "BERTHING_ONLY":
        irisan_str = ", ".join(d.strftime("%d %b %Y") for d in sorted(overlap_days))
        detail_li = "".join(
            f'<li><b>{c["STS_Mulai"].strftime("%d %b %Y")} – {c["STS_Selesai"].strftime("%d %b %Y")}</b> &bull; {c["Keterangan"]}</li>'
            for c in conflict_list
        )
        st.markdown(
            f'<div class="status-card status-warn">'
            f'<div style="font-size:1.05rem; font-weight:800;">⚠️ HANYA ASSIST BERTHING SAJA (TIDAK BISA UNBERTHING)</div>'
            f'Hari keberangkatan/berthing ajuan (<b>{tgl_ajuan.strftime("%d %b %Y")}</b>) masih aman, namun hari lanjutan '
            f'(s/d <b>{tgl_selesai_ajuan.strftime("%d %b %Y")}</b>) beririsan dengan jadwal STS FSRU NR pada: <b>{irisan_str}</b>.<br>'
            f'<b>Keputusan:</b> Diizinkan <b>Assist Berthing Only</b> pada jadwal ajuan, lalu Tugboat wajib segera kembali untuk STS FSRU NR.'
            f'<ul style="margin:6px 0 4px 18px;">{detail_li}</ul>'
            f'<span style="font-size:0.82rem; opacity:0.9;">{h5_note}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        irisan_str = ", ".join(d.strftime("%d %b %Y") for d in sorted(overlap_days))
        detail_li = "".join(
            f'<li><b>{c["STS_Mulai"].strftime("%d %b %Y")} – {c["STS_Selesai"].strftime("%d %b %Y")}</b> &bull; {c["Keterangan"]}</li>'
            for c in conflict_list
        )
        st.markdown(
            f'<div class="status-card status-danger">'
            f'<div style="font-size:1.05rem; font-weight:800;">🚫 TIDAK BISA SAMA SEKALI — BENTROK LANGSUNG HARI STS FSRU NR</div>'
            f'Tanggal mulai ajuan <b>{tgl_ajuan.strftime("%d %b %Y")}</b> jatuh tepat di dalam jendela operasi STS FSRU NR '
            f'(seluruh armada Tugboat wajib <i>standby</i> penuh di FSRU NR).<br>'
            f'<b>Hari Bentrok:</b> {irisan_str}'
            f'<ul style="margin:6px 0 4px 18px;">{detail_li}</ul>'
            f'<span style="font-size:0.82rem; opacity:0.9;">{h5_note}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    sts_df_vis = st.session_state.df_sts.copy()
    if not sts_df_vis.empty:
        sts_df_vis["Tanggal_Mulai"] = pd.to_datetime(sts_df_vis["Tanggal_Mulai"])
        sts_df_vis["Tanggal_Selesai"] = pd.to_datetime(sts_df_vis["Tanggal_Selesai"])
        sts_df_vis = sts_df_vis.sort_values("Tanggal_Mulai").reset_index(drop=True)

        fig_gantt = go.Figure()

        req_color = "#10b981" if status_code == "BISA" else ("#f59e0b" if status_code == "BERTHING_ONLY" else "#ef4444")
        req_lbl = "AJUAN ARMAKUNG"
        req_end_vis = pd.to_datetime(tgl_selesai_ajuan) + timedelta(days=1)
        fig_gantt.add_trace(go.Bar(
            y=[req_lbl],
            x=[(req_end_vis - pd.to_datetime(tgl_ajuan)).total_seconds() * 1000],
            base=[pd.to_datetime(tgl_ajuan)],
            orientation="h",
            marker=dict(color=req_color, line=dict(color="#ffffff", width=1.5)),
            text=[f"Ajuan: {tgl_ajuan.strftime('%d %b')}–{tgl_selesai_ajuan.strftime('%d %b')} ({durasi_ajuan} hr)"],
            textposition="inside",
            insidetextfont=dict(color="#ffffff", size=10, family="Segoe UI"),
            name="Ajuan ARMAKUNG",
            hovertemplate=f"<b>Ajuan ARMAKUNG</b><br>{tgl_ajuan.strftime('%d/%m/%Y')} – {tgl_selesai_ajuan.strftime('%d/%m/%Y')} ({durasi_ajuan} hari)<extra></extra>"
        ))

        conflict_set = {c["STS_Mulai"] for c in conflict_list}
        for _, r in sts_df_vis.iterrows():
            s0 = r["Tanggal_Mulai"]
            s1_vis = r["Tanggal_Selesai"] + timedelta(days=1)
            dur_ms = (s1_vis - s0).total_seconds() * 1000
            is_conf = s0.date() in conflict_set
            bar_clr = "#ef4444" if (is_conf and status_code == "TIDAK_BISA") else ("#f59e0b" if is_conf else "#00bcd4")
            fig_gantt.add_trace(go.Bar(
                y=[r["Keterangan"]],
                x=[dur_ms],
                base=[s0],
                orientation="h",
                marker=dict(color=bar_clr, opacity=0.9, line=dict(color="#67e8f9", width=1)),
                text=[f"{s0.strftime('%d %b')}–{r['Tanggal_Selesai'].strftime('%d %b')}"],
                textposition="inside",
                insidetextfont=dict(color="#041020", size=9.5, family="Segoe UI"),
                showlegend=False,
                hovertemplate=f"<b>{r['Keterangan']}</b><br>ETA: {s0.strftime('%d/%m/%Y')} – {r['Tanggal_Selesai'].strftime('%d/%m/%Y')}<extra></extra>"
            ))

        fig_gantt.update_layout(
            title=dict(text="Timeline Jadwal Cargo STS FSRU NR vs Ajuan ARMAKUNG", font=dict(size=12, color="#67e8f9")),
            barmode="overlay",
            paper_bgcolor=PLOT_BG,
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=FONT_CLR, size=10),
            height=max(260, 42 * (len(sts_df_vis) + 2)),
            margin=dict(l=10, r=20, t=38, b=30),
            xaxis=dict(type="date", gridcolor=GRID_CLR, tickformat="%d %b", automargin=True),
            yaxis=dict(autorange="reversed", gridcolor="rgba(255,255,255,0.06)", automargin=True),
            showlegend=False
        )
        st.plotly_chart(fig_gantt, use_container_width=True, config={"displayModeBar": False})

        today_dt = date.today()
        cards_parts = ['<div class="sts-grid">']
        for _, r in sts_df_vis.iterrows():
            s0_d = r["Tanggal_Mulai"].date()
            s1_d = r["Tanggal_Selesai"].date()
            dur_d = (s1_d - s0_d).days + 1
            is_conf = s0_d in conflict_set
            extra_cls = " sts-conflict" if (is_conf and status_code == "TIDAK_BISA") else (" sts-partial" if is_conf else "")

            if s1_d < today_dt:
                tag_html = '<span class="sts-tag sts-tag-done">SELESAI</span>'
            elif s0_d <= today_dt <= s1_d:
                tag_html = '<span class="sts-tag sts-tag-active">BERLANGSUNG</span>'
            else:
                diff = (s0_d - today_dt).days
                tag_html = f'<span class="sts-tag sts-tag-upcoming">H-{diff}</span>'

            cards_parts.append(
                f'<div class="sts-card{extra_cls}">'
                f'<div class="sts-badge-row">'
                f'<span class="sts-date-pill">ETA {s0_d.strftime("%d %b %Y")}</span>'
                f'{tag_html}'
                f'</div>'
                f'<div class="sts-vessel">🚢 {r["Keterangan"]}</div>'
                f'<div class="sts-window">Jendela STS: {s0_d.strftime("%d/%m")} – {s1_d.strftime("%d/%m/%Y")} ({dur_d} hari)</div>'
                f'</div>'
            )
        cards_parts.append('</div>')
        st.markdown("".join(cards_parts), unsafe_allow_html=True)

with tab_pdf:
    st.caption("Unggah PDF Cargo Schedule FSRU NR terbaru (format kolom ETA seperti '06-Nov', '04-Dec' otomatis terbaca). Dapat diunggah berulang kali setiap ada update bulanan.")
    if not HAS_PDFPLUMBER:
        st.warning("Library `pdfplumber` belum terpasang. Pastikan `pdfplumber>=0.10.0` ada di file `requirements.txt` di GitHub Anda.")

    up_c1, up_c2 = st.columns([1.8, 1.2])
    with up_c1:
        uploaded_pdf = st.file_uploader(
            "Pilih File PDF Cargo Schedule STS FSRU NR:",
            type=["pdf"],
            key=f"pdf_sts_uploader_{st.session_state.pdf_uploader_key}"
        )
    with up_c2:
        sync_mode = st.radio(
            "Mode Sinkronisasi:",
            ["Gabungkan & Perbarui (Merge)", "Ganti Seluruh Jadwal (Replace)"],
            index=0
        )
        p1, p2 = st.columns(2)
        scan_year = p1.number_input("Tahun Default", min_value=2025, max_value=2030, value=2026, step=1)
        sts_days = p2.number_input("Durasi STS (Hari)", min_value=1, max_value=5, value=3, step=1, help="Lama jendela operasi STS sejak tanggal ETA (default 3 hari: ETA s/d ETA+2)")

    if st.button("🔎 Upload & Scan Jadwal STS Baru", type="primary", use_container_width=True, disabled=(uploaded_pdf is None)):
        if uploaded_pdf is not None:
            scanned_rows, raw_debug = extract_sts_from_pdf(
                uploaded_pdf, default_year=int(scan_year), default_sts_days=int(sts_days)
            )
            if scanned_rows:
                df_new_sts = pd.DataFrame(scanned_rows)
                if sync_mode.startswith("Ganti"):
                    st.session_state.df_sts = df_new_sts.reset_index(drop=True)
                else:
                    combined = pd.concat([st.session_state.df_sts, df_new_sts], ignore_index=True)
                    combined["Tanggal_Mulai"] = pd.to_datetime(combined["Tanggal_Mulai"]).dt.date
                    combined["Tanggal_Selesai"] = pd.to_datetime(combined["Tanggal_Selesai"]).dt.date
                    combined = combined.drop_duplicates(subset=["Tanggal_Mulai", "Tanggal_Selesai"], keep="last")
                    combined = combined.sort_values("Tanggal_Mulai").reset_index(drop=True)
                    st.session_state.df_sts = combined

                st.session_state.pdf_scan_history.append({
                    "Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "File": uploaded_pdf.name,
                    "Mode": sync_mode,
                    "Jumlah_Cargo": len(scanned_rows)
                })
                st.session_state.pdf_uploader_key += 1
                st.success(f"Berhasil memindai {len(scanned_rows)} jadwal Cargo STS dari '{uploaded_pdf.name}' dan menyinkronkannya ke sistem!")
                st.rerun()
            else:
                st.warning(
                    "Tidak ditemukan pola tanggal ETA pada PDF tersebut (kemungkinan PDF berupa hasil scan gambar). "
                    "Anda tetap dapat menginput jadwal manual di tab 'Edit Manual Jadwal STS'."
                )
                with st.expander("Lihat teks mentah hasil pembacaan PDF"):
                    st.text(raw_debug[:2500] if raw_debug else "(Kosong)")

    if st.session_state.pdf_scan_history:
        st.markdown("**Riwayat Sinkronisasi PDF:**")
        st.dataframe(pd.DataFrame(st.session_state.pdf_scan_history), use_container_width=True, hide_index=True)

with tab_sts_tbl:
    st.caption("Edit, tambah, atau hapus jadwal Cargo STS FSRU NR secara langsung.")
    sts_edit_df = st.data_editor(
        st.session_state.df_sts,
        num_rows="dynamic",
        use_container_width=True,
        height=280,
        column_config={
            "Tanggal_Mulai": st.column_config.DateColumn("Tanggal ETA / Mulai STS", format="DD/MM/YYYY", required=True),
            "Tanggal_Selesai": st.column_config.DateColumn("Tanggal Selesai STS", format="DD/MM/YYYY", required=True),
            "Keterangan": st.column_config.TextColumn("LNGC & Cargo No."),
            "Sumber": st.column_config.TextColumn("Sumber Update"),
        },
        key="editor_sts_schedule"
    )
    sc1, sc2, sc3 = st.columns([1.2, 1.2, 1.6])
    with sc1:
        if st.button("💾 Simpan Perubahan Jadwal STS", type="primary", use_container_width=True):
            cleaned_sts = sts_edit_df.dropna(subset=["Tanggal_Mulai", "Tanggal_Selesai"]).reset_index(drop=True)
            st.session_state.df_sts = cleaned_sts
            st.success("Jadwal STS FSRU NR berhasil disimpan!")
            st.rerun()
    with sc2:
        st.download_button(
            "⬇️ Unduh Jadwal STS (CSV)",
            data=st.session_state.df_sts.to_csv(index=False).encode("utf-8"),
            file_name="Jadwal_STS_FSRU_NR_2026.csv",
            mime="text/csv",
            use_container_width=True
        )
    with sc3:
        if st.button("🔄 Reset Jadwal Nov–Des 2026", use_container_width=True):
            st.session_state.df_sts = pd.DataFrame(INITIAL_STS_SCHEDULE)
            st.rerun()

# ==============================================================================
# BARIS 5: INPUT 2 — UPDATE DATA REKAP PASCA-ASSIST (TERPISAH DARI CEK BENTROK)
# ==============================================================================
st.markdown('<div class="panel-header">✏️ INPUT 2 — Update Data Rekap Realisasi Pasca-Assist (Tambah, Edit &amp; Hapus)</div>', unsafe_allow_html=True)

tab_add, tab_edit = st.tabs(["➕ Input Realisasi Pasca-Assist (Auto-Hitung)", "📝 Edit / Hapus Rekap 2026"])

with tab_add:
    st.caption("Gunakan form ini **setelah kegiatan assist selesai** untuk mencatat realisasi sewa, konsumsi BBM (HSD), dan memperbarui KPI pendapatan secara otomatis.")
    with st.form("form_tambah_call", clear_on_submit=True):
        f1, f2, f3, f4 = st.columns(4)
        in_bulan = f1.selectbox("Bulan", MONTH_LIST, index=10)
        in_kapal = f2.selectbox("Nama Kapal", VESSEL_LIST)
        in_del = f3.text_input("Tgl Delivery", value="10/11/2026")
        in_red = f4.text_input("Tgl Re-delivery", value="13/11/2026")

        f5, f6, f7, f8 = st.columns(4)
        in_dur = f5.number_input("Durasi Aktual (Hari)", min_value=0.1, max_value=10.0, value=3.00, step=0.05)
        in_hsd_l = f6.number_input("Konsumsi HSD (Liter)", min_value=0, max_value=20000, value=7800, step=100)
        in_hrg = f7.number_input("Harga HSD (Rp/Liter)", min_value=0, max_value=50000, value=17755, step=100)
        in_tarif = f8.number_input("Tarif Sewa (Rp/Hari)", min_value=0, max_value=100000000, value=49000000, step=500000)

        if st.form_submit_button("💾 Simpan Realisasi Assist ke Rekap Dashboard", type="primary", use_container_width=True):
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
            st.success(f"Realisasi assist ({in_kapal} - {in_bulan}) berhasil ditambahkan ke rekap!")
            st.rerun()

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
            "⬇️ Unduh Data Rekap (CSV)",
            data=st.session_state.df_data.to_csv(index=False).encode("utf-8"),
            file_name="Data_ARMAKUNG_2026_Updated.csv",
            mime="text/csv",
            use_container_width=True
        )
