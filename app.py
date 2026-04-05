import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io, time

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AnomalyIQ",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #05080f !important;
    color: #d1d5db !important;
}
#MainMenu, footer, header { display: none !important; }
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 100% !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #070a14 !important;
    border-right: 1px solid #0f1721 !important;
    padding: 0 !important;
}
section[data-testid="stSidebar"] > div { padding: 1.5rem 1.2rem !important; }
section[data-testid="stSidebar"] .stMarkdown p { color: #6b7280 !important; font-size: 0.82rem; }
section[data-testid="stSidebar"] label { color: #9ca3af !important; font-size: 0.82rem !important; }

/* ── Page header ── */
.pg-header {
    padding: 0.5rem 0 1.5rem 0;
    border-bottom: 1px solid #0f1721;
    margin-bottom: 1.8rem;
}
.pg-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(20,184,166,0.08);
    border: 1px solid rgba(20,184,166,0.18);
    border-radius: 20px; padding: 3px 11px;
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: #14b8a6; margin-bottom: 0.8rem;
}
.pg-dot { width:5px; height:5px; background:#14b8a6; border-radius:50%; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
.pg-header h1 {
    font-size: 1.7rem; font-weight: 800;
    letter-spacing: -0.035em; color: #f9fafb; margin: 0.3rem 0 0.4rem 0;
}
.pg-header h1 span {
    background: linear-gradient(90deg, #14b8a6, #2dd4bf 50%, #f59e0b);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.pg-header p { font-size: 0.88rem; color: #6b7280; margin: 0; }

/* ── Section blocks ── */
.sec-label {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.15em;
    text-transform: uppercase; color: #374151; margin-bottom: 0.5rem;
}
.sec-title {
    font-size: 1rem; font-weight: 700; color: #e5e7eb;
    margin: 0 0 1rem 0; letter-spacing: -0.01em;
}

/* ── Cards ── */
.card {
    background: #090d18; border: 1px solid #0f1721;
    border-radius: 12px; padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.card-title {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: #374151; margin-bottom: 0.8rem;
}

/* ── Stat grid ── */
.stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 0.8rem; margin-bottom:1.5rem; }
.stat { background:#090d18; border:1px solid #0f1721; border-radius:12px; padding:1.1rem 1.2rem; position:relative; overflow:hidden; }
.stat::before { content:''; position:absolute; top:0;left:0;right:0; height:2px; }
.stat.teal::before  { background: linear-gradient(90deg,#14b8a6,#2dd4bf); }
.stat.rose::before  { background: linear-gradient(90deg,#f43f5e,#fb7185); }
.stat.amber::before { background: linear-gradient(90deg,#f59e0b,#fbbf24); }
.stat.violet::before{ background: linear-gradient(90deg,#8b5cf6,#a78bfa); }
.stat-l { font-size:0.6rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#4b5563; margin-bottom:0.4rem; }
.stat-v { font-size:1.8rem; font-weight:900; letter-spacing:-0.04em; color:#f9fafb; line-height:1; }
.stat-s { font-size:0.68rem; color:#4b5563; margin-top:0.25rem; }

/* ── Insight cards ── */
.insight {
    background:#090d18; border:1px solid #0f1721;
    border-radius:10px; padding:0.9rem 1.1rem; margin-bottom:0.7rem;
    font-size:0.83rem; color:#6b7280; line-height:1.7;
}
.insight.spike { border-left:3px solid #f43f5e; }
.insight.drop  { border-left:3px solid #8b5cf6; }
.insight.info  { border-left:3px solid #14b8a6; }
.insight.warn  { border-left:3px solid #f59e0b; }
.insight strong { color:#d1d5db; font-weight:600; }
.itag {
    display:inline-block; border-radius:4px;
    font-size:0.58rem; font-weight:700; letter-spacing:0.08em; padding:2px 7px;
    text-transform:uppercase; margin-bottom:0.35rem;
}
.itag.teal   { background:rgba(20,184,166,0.1);  border:1px solid rgba(20,184,166,0.2);  color:#14b8a6; }
.itag.rose   { background:rgba(244,63,94,0.1);   border:1px solid rgba(244,63,94,0.2);   color:#f43f5e; }
.itag.violet { background:rgba(139,92,246,0.1);  border:1px solid rgba(139,92,246,0.2);  color:#a78bfa; }
.itag.amber  { background:rgba(245,158,11,0.1);  border:1px solid rgba(245,158,11,0.2);  color:#f59e0b; }

/* ── Table ── */
div[data-testid="stDataFrame"] {
    border: 1px solid #0f1721 !important;
    border-radius: 10px !important; overflow: hidden !important;
}

/* ── Uploader ── */
div[data-testid="stFileUploader"] > div,
div[data-testid="stFileUploader"] > div > div,
div[data-testid="stFileUploaderDropzone"] {
    background: #090d18 !important;
    border: 1.5px dashed #1a2235 !important;
    border-radius: 12px !important;
}
div[data-testid="stFileUploader"] > div:hover { border-color: #14b8a6 !important; }
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] small { color: #6b7280 !important; }
div[data-testid="stFileUploader"] button {
    background: #0d1a17 !important; color: #14b8a6 !important;
    border: 1px solid #14b8a6 !important; border-radius: 7px !important;
    font-weight: 600 !important; font-size: 0.78rem !important;
}
div[data-testid="stFileUploader"] button:hover {
    background: #14b8a6 !important; color: #05080f !important;
}

/* ── Slider ── */
div[data-baseweb="slider"] [role="slider"] { background: #14b8a6 !important; border-color: #14b8a6 !important; }
div[data-testid="stSlider"] label { color: #9ca3af !important; }

/* ── Download button ── */
div[data-testid="stDownloadButton"] > button {
    background: #0d1a17 !important; color: #14b8a6 !important;
    border: 1px solid #14b8a6 !important; border-radius: 8px !important;
    font-size: 0.8rem !important; font-weight: 600 !important;
    width: 100% !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #14b8a6 !important; color: #05080f !important;
}

/* ── Success / error ── */
div[data-testid="stAlert"] { border-radius: 9px !important; }

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: #090d18 !important; border: 1px solid #0f1721 !important;
    border-radius: 10px !important;
}
div[data-testid="stExpander"] summary { color: #6b7280 !important; font-size: 0.82rem !important; }

/* ── Divider ── */
hr { border: none; border-top: 1px solid #0f1721; margin: 1.5rem 0; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #05080f; }
::-webkit-scrollbar-thumb { background: #111827; border-radius: 3px; }

/* ── Sidebar step ── */
.step { display:flex; align-items:flex-start; gap:0.7rem; margin-bottom:0.9rem; }
.step-n {
    background:#0f1929; color:#14b8a6;
    font-size:0.65rem; font-weight:800;
    border-radius:5px; width:20px; height:20px;
    display:flex; align-items:center; justify-content:center;
    flex-shrink:0; margin-top:1px;
}
.step-t { font-size:0.8rem; font-weight:600; color:#9ca3af; }
.step-d { font-size:0.73rem; color:#4b5563; margin-top:1px; line-height:1.45; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;
                    color:#14b8a6;font-weight:700;margin-bottom:0.4rem;">AnomalyIQ</div>
        <div style="font-size:1.05rem;font-weight:800;color:#f9fafb;letter-spacing:-0.03em;">
            Anomaly Detector</div>
        <div style="font-size:0.75rem;color:#374151;margin-top:0.2rem;">Statistical Z-Score Engine</div>
    </div>
    <hr style="border-top:1px solid #0f1721;margin:0 0 1.3rem 0;">
    """, unsafe_allow_html=True)

    # Steps guide
    st.markdown("""
    <div style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;
                color:#374151;font-weight:700;margin-bottom:0.8rem;">How to Use</div>
    <div class="step">
        <div class="step-n">1</div>
        <div><div class="step-t">Upload CSV</div>
        <div class="step-d">File with <code style="background:#0f1721;padding:1px 4px;border-radius:3px;color:#14b8a6;font-size:0.7rem;">Date</code>
        and <code style="background:#0f1721;padding:1px 4px;border-radius:3px;color:#14b8a6;font-size:0.7rem;">Value</code> columns</div></div>
    </div>
    <div class="step">
        <div class="step-n">2</div>
        <div><div class="step-t">Adjust Threshold</div>
        <div class="step-d">Control sensitivity — lower flags more anomalies</div></div>
    </div>
    <div class="step">
        <div class="step-n">3</div>
        <div><div class="step-t">Filter & Explore</div>
        <div class="step-d">Use the date range filter and review results</div></div>
    </div>
    <div class="step">
        <div class="step-n">4</div>
        <div><div class="step-t">Export Report</div>
        <div class="step-d">Download anomaly results as CSV</div></div>
    </div>
    <hr style="border-top:1px solid #0f1721;margin:1rem 0;">
    """, unsafe_allow_html=True)

    # Threshold slider
    st.markdown('<div style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#374151;font-weight:700;margin-bottom:0.4rem;">Z-Score Threshold</div>', unsafe_allow_html=True)
    threshold = st.slider("threshold", min_value=1.0, max_value=4.0,
                          value=2.0, step=0.1, label_visibility="collapsed")
    st.markdown(f'<div style="font-size:0.7rem;color:#4b5563;margin-top:0.2rem;">Flag rows where |Z| > <strong style="color:#14b8a6;">{threshold:.1f}</strong></div>', unsafe_allow_html=True)

    st.markdown('<hr style="border-top:1px solid #0f1721;margin:1rem 0;">', unsafe_allow_html=True)

    # Upload section in sidebar
    st.markdown('<div style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#374151;font-weight:700;margin-bottom:0.6rem;">Upload Data</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("upload", type=["csv"], label_visibility="collapsed")
    st.markdown('<div style="font-size:0.7rem;color:#374151;margin-top:0.3rem;">CSV · <span style="color:#14b8a6;">Date</span> + <span style="color:#14b8a6;">Value</span> columns required</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# MAIN AREA
# ═══════════════════════════════════════════════════

# Page header
st.markdown("""
<div class="pg-header">
    <div class="pg-badge"><div class="pg-dot"></div>Z-Score Detection · Live</div>
    <h1>Anomaly Detection & <span>Root Cause Analyzer</span></h1>
    <p>Upload time-series CSV data to detect outliers, visualize patterns, and understand root causes instantly.</p>
</div>
""", unsafe_allow_html=True)

# ─── No file state ───────────────────────────────────────────────────────────────
if uploaded_file is None:
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;">
        <div style="font-size:2.5rem;opacity:0.15;margin-bottom:1rem;">◈</div>
        <div style="font-size:1rem;font-weight:600;color:#374151;margin-bottom:0.4rem;">No data uploaded yet</div>
        <div style="font-size:0.82rem;color:#1f2937;">Upload a CSV from the sidebar to begin.</div>
    </div>
    """, unsafe_allow_html=True)

    # Show example format
    st.markdown('<div class="sec-label">Expected CSV Format</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        example = pd.DataFrame({
            "Date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "Value": [120, 115, 118, 950, 122],
        })
        st.dataframe(example, use_container_width=True, hide_index=True)
        st.markdown('<div style="font-size:0.72rem;color:#374151;text-align:center;margin-top:0.4rem;">Row 4 would be flagged as an anomaly (spike)</div>', unsafe_allow_html=True)
    st.stop()

# ─── Load & validate ─────────────────────────────────────────────────────────────
try:
    raw_df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Could not read file: {e}")
    st.stop()

if "Date" not in raw_df.columns or "Value" not in raw_df.columns:
    st.error("Your CSV must contain columns named **Date** and **Value**. Please re-upload.")
    st.stop()

raw_df["Date"]  = pd.to_datetime(raw_df["Date"], errors="coerce")
raw_df["Value"] = pd.to_numeric(raw_df["Value"], errors="coerce")

bad_rows = raw_df[["Date", "Value"]].isna().any(axis=1).sum()
if bad_rows > 0:
    st.warning(f"{bad_rows} row(s) with invalid Date or Value were removed automatically.")

raw_df = raw_df.dropna(subset=["Date", "Value"]).reset_index(drop=True)

if raw_df.empty:
    st.error("No valid data rows remain after cleaning. Please check your file.")
    st.stop()

# Success toast
st.success(f"Loaded **{len(raw_df):,} rows** successfully — {raw_df['Date'].min().strftime('%b %d, %Y')} to {raw_df['Date'].max().strftime('%b %d, %Y')}")

# ─── Date range filter ──────────────────────────────────────────────────────────
st.markdown('<div class="sec-label" style="margin-top:1.2rem;">Date Range Filter</div>', unsafe_allow_html=True)

date_min = raw_df["Date"].min().date()
date_max = raw_df["Date"].max().date()

fc1, fc2, fc3 = st.columns([2, 2, 3])
with fc1:
    start_date = st.date_input("From", value=date_min, min_value=date_min, max_value=date_max)
with fc2:
    end_date = st.date_input("To", value=date_max, min_value=date_min, max_value=date_max)
with fc3:
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.78rem;color:#6b7280;padding-top:0.9rem;">Showing data from <strong style="color:#d1d5db;">{start_date}</strong> to <strong style="color:#d1d5db;">{end_date}</strong></div>', unsafe_allow_html=True)

if start_date > end_date:
    st.error("'From' date must be before 'To' date.")
    st.stop()

df = raw_df[(raw_df["Date"].dt.date >= start_date) & (raw_df["Date"].dt.date <= end_date)].copy()

if df.empty:
    st.warning("No data in selected date range. Adjust the filter above.")
    st.stop()

# ─── Z-Score Detection (core logic — unchanged) ─────────────────────────────────
with st.spinner("Analyzing data..."):
    time.sleep(0.3)  # brief loading feedback

    mean_val = df["Value"].mean()
    std_val  = df["Value"].std()
    min_val  = df["Value"].min()
    max_val  = df["Value"].max()

    if std_val == 0 or pd.isna(std_val):
        df["Z_Score"] = 0.0
    else:
        df["Z_Score"] = (df["Value"] - mean_val) / std_val

    df["Is_Anomaly"] = df["Z_Score"].abs() > threshold

    def get_reason(z):
        if z >  threshold: return "Spike — significantly above average"
        if z < -threshold: return "Drop — significantly below average"
        return "Normal"

    df["Reason"] = df["Z_Score"].apply(get_reason)

anomalies_df    = df[df["Is_Anomaly"]].copy()
total_records   = len(df)
total_anomalies = int(df["Is_Anomaly"].sum())
anomaly_rate    = (total_anomalies / total_records * 100) if total_records else 0

# ═══════════════════════════════════════════════════
# SECTION: Analysis Results
# ═══════════════════════════════════════════════════
st.markdown('<hr><div class="sec-label">Analysis Results</div><div class="sec-title">Summary Statistics</div>', unsafe_allow_html=True)

# Stat cards
st.markdown(f"""
<div class="stat-grid">
    <div class="stat teal">
        <div class="stat-l">Records Analyzed</div>
        <div class="stat-v">{total_records:,}</div>
        <div class="stat-s">in selected range</div>
    </div>
    <div class="stat rose">
        <div class="stat-l">Anomalies Found</div>
        <div class="stat-v">{total_anomalies}</div>
        <div class="stat-s">|Z| &gt; {threshold:.1f}</div>
    </div>
    <div class="stat amber">
        <div class="stat-l">Anomaly Rate</div>
        <div class="stat-v">{anomaly_rate:.1f}%</div>
        <div class="stat-s">of filtered data</div>
    </div>
    <div class="stat violet">
        <div class="stat-l">Std Deviation</div>
        <div class="stat-v">{std_val:,.1f}</div>
        <div class="stat-s">mean: {mean_val:,.1f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Additional stats row
sc1, sc2, sc3, sc4 = st.columns(4)
sc1.metric("Min Value",    f"{min_val:,.2f}")
sc2.metric("Max Value",    f"{max_val:,.2f}")
sc3.metric("Value Range",  f"{max_val - min_val:,.2f}")
sc4.metric("Z Threshold",  f"±{threshold:.1f}σ")

# ═══════════════════════════════════════════════════
# SECTION: Chart
# ═══════════════════════════════════════════════════
st.markdown('<hr><div class="sec-label">Visualization</div><div class="sec-title">Time Series — Anomalies Highlighted</div>', unsafe_allow_html=True)

BG = "#090d18"
col_chart, col_hist = st.columns([3, 1], gap="medium")

with col_chart:
    fig, ax = plt.subplots(figsize=(11, 4))
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

    upper = mean_val + threshold * std_val
    lower = mean_val - threshold * std_val

    # Fill under line
    ax.fill_between(df["Date"], df["Value"], min_val,
                    color="#14b8a6", alpha=0.05, zorder=1)
    # Main line
    ax.plot(df["Date"], df["Value"],
            color="#14b8a6", linewidth=1.6, alpha=0.85,
            zorder=2, label="Normal")
    # Threshold bands
    ax.axhspan(upper, max_val * 1.08, color="#f43f5e", alpha=0.04, zorder=0)
    ax.axhspan(min_val * 0.92, lower, color="#8b5cf6", alpha=0.04, zorder=0)
    ax.axhline(upper, color="#f43f5e", linewidth=0.6, linestyle=":", alpha=0.4, zorder=1)
    ax.axhline(lower, color="#8b5cf6", linewidth=0.6, linestyle=":", alpha=0.4, zorder=1)
    ax.axhline(mean_val, color="#1f2937", linewidth=0.9, linestyle="--",
               alpha=0.7, zorder=1, label=f"Mean ({mean_val:.1f})")

    # Anomaly points
    spikes = anomalies_df[anomalies_df["Z_Score"] > 0]
    drops  = anomalies_df[anomalies_df["Z_Score"] < 0]
    if not spikes.empty:
        ax.scatter(spikes["Date"], spikes["Value"], color="#f43f5e", s=50, zorder=5,
                   edgecolors="#fda4af", linewidth=0.7, label="Spike")
    if not drops.empty:
        ax.scatter(drops["Date"], drops["Value"], color="#8b5cf6", s=50, zorder=5,
                   edgecolors="#c4b5fd", linewidth=0.7, label="Drop")

    for sp in ax.spines.values(): sp.set_color("#0f1721")
    ax.tick_params(colors="#4b5563", labelsize=8)
    ax.set_xlabel("Date",  fontsize=8.5, color="#4b5563", labelpad=6)
    ax.set_ylabel("Value", fontsize=8.5, color="#4b5563", labelpad=6)
    ax.grid(axis="y", alpha=0.06, color="#14b8a6", linewidth=0.5)
    ax.grid(axis="x", alpha=0.04, color="#4b5563", linewidth=0.5)
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(mdates.AutoDateLocator()))
    fig.autofmt_xdate(rotation=28)
    ax.legend(fontsize=8, framealpha=0.15, facecolor="#05080f",
              edgecolor="#0f1721", labelcolor="#6b7280",
              loc="upper left")
    plt.tight_layout(pad=1.2)
    st.pyplot(fig)

with col_hist:
    fig2, ax2 = plt.subplots(figsize=(3.5, 4))
    fig2.patch.set_facecolor(BG); ax2.set_facecolor(BG)

    normal_v = df.loc[~df["Is_Anomaly"], "Value"]
    anom_v   = df.loc[ df["Is_Anomaly"], "Value"]
    bins     = min(25, max(8, total_records // 5))

    ax2.hist(normal_v, bins=bins, color="#14b8a6", alpha=0.5,
             edgecolor=BG, linewidth=0.3, label="Normal")
    if len(anom_v):
        ax2.hist(anom_v, bins=bins, color="#f43f5e", alpha=0.65,
                 edgecolor=BG, linewidth=0.3, label="Anomaly")

    ax2.axvline(mean_val, color="#f59e0b", linewidth=1.3, linestyle="--", label="Mean")

    for sp in ax2.spines.values(): sp.set_color("#0f1721")
    ax2.tick_params(colors="#4b5563", labelsize=7.5)
    ax2.set_xlabel("Value",  fontsize=8, color="#4b5563")
    ax2.set_ylabel("Count",  fontsize=8, color="#4b5563")
    ax2.set_title("Distribution", fontsize=8.5, color="#6b7280", pad=6)
    ax2.grid(axis="y", alpha=0.05, color="#14b8a6")
    ax2.grid(axis="x", alpha=0)
    ax2.legend(fontsize=7, framealpha=0.12, facecolor="#05080f",
               edgecolor="#0f1721", labelcolor="#6b7280")
    plt.tight_layout(pad=1.2)
    st.pyplot(fig2)

# ═══════════════════════════════════════════════════
# SECTION: Anomaly Table + Export
# ═══════════════════════════════════════════════════
st.markdown('<hr>', unsafe_allow_html=True)
tcol, dcol = st.columns([4, 1])
with tcol:
    st.markdown(f'<div class="sec-label">Flagged Records — {total_anomalies} anomalies</div>', unsafe_allow_html=True)
with dcol:
    st.markdown("<div style='height:0.1rem'></div>", unsafe_allow_html=True)

if total_anomalies > 0:
    show_df = anomalies_df[["Date", "Value", "Z_Score", "Reason"]].copy()
    show_df["Date"]    = show_df["Date"].dt.strftime("%Y-%m-%d")
    show_df["Value"]   = show_df["Value"].round(2)
    show_df["Z_Score"] = show_df["Z_Score"].round(3)
    show_df.rename(columns={"Z_Score": "Z-Score", "Reason": "Root Cause"}, inplace=True)

    with dcol:
        csv_bytes = show_df.to_csv(index=False).encode()
        st.download_button(
            label="⬇ Export CSV",
            data=csv_bytes,
            file_name="anomaly_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.dataframe(show_df.reset_index(drop=True), use_container_width=True,
                 height=min(350, 48 + 36 * total_anomalies))
else:
    st.markdown("""
    <div style="background:rgba(20,184,166,0.05);border:1px solid rgba(20,184,166,0.15);
                border-radius:10px;padding:1rem 1.3rem;font-size:0.84rem;color:#14b8a6;">
        No anomalies detected at the current threshold — all values are statistically normal.
    </div>""", unsafe_allow_html=True)

with st.expander("View raw data (all rows)"):
    st.dataframe(df.head(200), use_container_width=True)

# ═══════════════════════════════════════════════════
# SECTION: AI Insights
# ═══════════════════════════════════════════════════
st.markdown('<hr><div class="sec-label">AI Insights</div><div class="sec-title">Root Cause Analysis</div>', unsafe_allow_html=True)

if total_anomalies == 0:
    st.markdown("""<div class="insight info">
        <div class="itag teal">Healthy</div><br>
        <strong>No anomalies detected.</strong> The dataset is statistically stable — all values fall within
        the chosen threshold. Try lowering the Z-score slider in the sidebar to increase sensitivity.
    </div>""", unsafe_allow_html=True)
else:
    spk = anomalies_df[anomalies_df["Z_Score"] > 0]
    drp = anomalies_df[anomalies_df["Z_Score"] < 0]

    # Spike insight
    if not spk.empty:
        w   = spk.loc[spk["Z_Score"].idxmax()]
        pct = ((w["Value"] - mean_val) / abs(mean_val)) * 100 if mean_val != 0 else 0
        multi = "Multiple spikes detected — " if len(spk) > 1 else ""
        st.markdown(f"""<div class="insight spike">
            <div class="itag rose">Spike · {len(spk)} event(s)</div><br>
            <strong>{multi}Largest on {w['Date'].strftime('%Y-%m-%d')}</strong> — value hit
            <strong>{w['Value']:,.2f}</strong> ({pct:+.1f}% vs mean of {mean_val:,.1f}).
            Z-score: <strong>{w['Z_Score']:.2f}</strong>.
            Investigate for promotions, system bursts, or data entry errors at this date.
        </div>""", unsafe_allow_html=True)

    # Drop insight
    if not drp.empty:
        w   = drp.loc[drp["Z_Score"].idxmin()]
        pct = ((w["Value"] - mean_val) / abs(mean_val)) * 100 if mean_val != 0 else 0
        multi = "Multiple drops detected — " if len(drp) > 1 else ""
        st.markdown(f"""<div class="insight drop">
            <div class="itag violet">Drop · {len(drp)} event(s)</div><br>
            <strong>{multi}Largest on {w['Date'].strftime('%Y-%m-%d')}</strong> — value fell to
            <strong>{w['Value']:,.2f}</strong> ({pct:+.1f}% vs mean of {mean_val:,.1f}).
            Z-score: <strong>{w['Z_Score']:.2f}</strong>.
            Possible causes: outages, data loss, reduced activity, or pipeline failures.
        </div>""", unsafe_allow_html=True)

    # Pattern insight
    if total_anomalies > 3:
        st.markdown(f"""<div class="insight warn">
            <div class="itag amber">Pattern</div><br>
            <strong>Multiple anomalies observed</strong> — {total_anomalies} outliers across
            {total_records:,} records ({anomaly_rate:.1f}%). This may indicate a
            <strong>systematic issue</strong> rather than isolated events.
            {'Consider raising the threshold if these are expected variations.' if anomaly_rate < 20
             else 'High anomaly rate — consider auditing your data pipeline.'}
        </div>""", unsafe_allow_html=True)

    # Range / overview insight
    st.markdown(f"""<div class="insight info">
        <div class="itag teal">Overview</div><br>
        <strong>Dataset range:</strong> {min_val:,.1f} to {max_val:,.1f}
        (spread: {max_val - min_val:,.1f}).
        Mean: <strong>{mean_val:,.1f}</strong> · Std dev: <strong>{std_val:,.1f}</strong> · 
        Threshold: <strong>±{threshold:.1f}σ</strong>.
        Period covers <strong>{(df['Date'].max() - df['Date'].min()).days + 1} days</strong>.
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:2.5rem;'></div>", unsafe_allow_html=True)
