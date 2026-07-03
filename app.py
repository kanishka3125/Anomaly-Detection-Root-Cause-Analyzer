import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AnomalyIQ",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Session State ─────────────────────────────────────────────────────────────
if "started" not in st.session_state:
    st.session_state.started = False

# ─── CSS (Sky Blue Theme - Light) ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #f4f9fd !important;
    color: #0f172a !important;
}
#MainMenu, footer, header { display: none !important; }
.block-container { padding: 1.5rem 2rem 2rem 2rem !important; max-width: 100% !important; }

/* ── Animations ── */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
.slide-up { animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.fade-in { animation: fadeIn 0.6s ease-in-out forwards; }

/* ── Landing Page ── */
.landing-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 70vh;
    text-align: center;
}
.landing-title {
    font-size: 6rem;
    font-weight: 900;
    letter-spacing: -0.04em;
    background: linear-gradient(90deg, #0ea5e9, #38bdf8 40%, #0284c7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
    line-height: 1.1;
}
.landing-subtitle {
    font-size: 1.3rem;
    color: #64748b;
    font-weight: 500;
    margin-bottom: 2.5rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
}

/* ── Primary Button (Landing) ── */
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #0ea5e9, #0284c7) !important;
    color: white !important;
    border: none !important;
    padding: 0.6rem 2.5rem !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    border-radius: 50px !important;
    box-shadow: 0 4px 14px rgba(14, 165, 233, 0.3) !important;
    transition: all 0.3s ease !important;
}
div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(14, 165, 233, 0.5) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    padding: 0 !important;
}
section[data-testid="stSidebar"] > div { padding: 1.5rem 1.2rem !important; }
section[data-testid="stSidebar"] .stMarkdown p { color: #475569 !important; font-size: 0.82rem; }
section[data-testid="stSidebar"] label { color: #334155 !important; font-size: 0.82rem !important; }

/* ── Page header ── */
.pg-header {
    padding: 0.5rem 0 1.5rem 0;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 1.8rem;
}
.pg-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(14, 165, 233, 0.08);
    border: 1px solid rgba(14, 165, 233, 0.2);
    border-radius: 20px; padding: 3px 11px;
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: #0284c7; margin-bottom: 0.8rem;
}
.pg-dot { width:5px; height:5px; background:#0ea5e9; border-radius:50%; animation: blink 2s infinite; }
.pg-header h1 {
    font-size: 1.7rem; font-weight: 800;
    letter-spacing: -0.035em; color: #0f172a; margin: 0.3rem 0 0.4rem 0;
}
.pg-header h1 span {
    background: linear-gradient(90deg, #0ea5e9, #38bdf8 50%, #0369a1);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.pg-header p { font-size: 0.88rem; color: #475569; margin: 0; }

/* ── Section blocks ── */
.sec-label {
    font-size: 0.6rem; font-weight: 700; letter-spacing: 0.15em;
    text-transform: uppercase; color: #64748b; margin-bottom: 0.5rem;
}
.sec-title {
    font-size: 1rem; font-weight: 700; color: #0f172a;
    margin: 0 0 1rem 0; letter-spacing: -0.01em;
}

/* ── Stat grid ── */
.stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 0.8rem; margin-bottom:1.5rem; }
.stat { background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:1.1rem 1.2rem; position:relative; overflow:hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
.stat::before { content:''; position:absolute; top:0;left:0;right:0; height:3px; }
.stat.sky::before  { background: linear-gradient(90deg,#0ea5e9,#38bdf8); }
.stat.rose::before  { background: linear-gradient(90deg,#ef4444,#f87171); }
.stat.amber::before { background: linear-gradient(90deg,#f59e0b,#fbbf24); }
.stat.indigo::before{ background: linear-gradient(90deg,#6366f1,#818cf8); }
.stat-l { font-size:0.6rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#64748b; margin-bottom:0.4rem; }
.stat-v { font-size:1.8rem; font-weight:900; letter-spacing:-0.04em; color:#0f172a; line-height:1; }
.stat-s { font-size:0.68rem; color:#64748b; margin-top:0.25rem; }

/* ── Insight cards ── */
.insight {
    background:#ffffff; border:1px solid #e2e8f0;
    border-radius:10px; padding:0.9rem 1.1rem; margin-bottom:0.7rem;
    font-size:0.83rem; color:#475569; line-height:1.7;
    box-shadow: 0 1px 2px rgba(0,0,0,0.01);
}
.insight.spike { border-left:3px solid #ef4444; }
.insight.drop  { border-left:3px solid #6366f1; }
.insight.info  { border-left:3px solid #0ea5e9; }
.insight.warn  { border-left:3px solid #f59e0b; }
.insight strong { color:#0f172a; font-weight:600; }
.itag {
    display:inline-block; border-radius:4px;
    font-size:0.58rem; font-weight:700; letter-spacing:0.08em; padding:2px 7px;
    text-transform:uppercase; margin-bottom:0.35rem;
}
.itag.sky   { background:rgba(14,165,233,0.1);  border:1px solid rgba(14,165,233,0.2);  color:#0284c7; }
.itag.rose   { background:rgba(239,68,68,0.1);   border:1px solid rgba(239,68,68,0.2);   color:#dc2626; }
.itag.indigo { background:rgba(99,102,241,0.1);  border:1px solid rgba(99,102,241,0.2);  color:#4f46e5; }
.itag.amber  { background:rgba(245,158,11,0.1);  border:1px solid rgba(245,158,11,0.2);  color:#d97706; }

/* ── Table ── */
div[data-testid="stDataFrame"] { border: 1px solid #e2e8f0 !important; border-radius: 10px !important; overflow: hidden !important; }

/* ── Uploader ── */
div[data-testid="stFileUploader"] > div, div[data-testid="stFileUploader"] > div > div, div[data-testid="stFileUploaderDropzone"] {
    background: #f8fafc !important; border: 1.5px dashed #cbd5e1 !important; border-radius: 12px !important;
}
div[data-testid="stFileUploader"] > div:hover { border-color: #0ea5e9 !important; }
div[data-testid="stFileUploader"] span, div[data-testid="stFileUploader"] small { color: #64748b !important; }
div[data-testid="stFileUploader"] button {
    background: #e0f2fe !important; color: #0284c7 !important; border: 1px solid #7dd3fc !important; border-radius: 7px !important; font-weight: 600 !important; font-size: 0.78rem !important;
}
div[data-testid="stFileUploader"] button:hover { background: #0ea5e9 !important; color: #ffffff !important; }

/* ── Slider ── */
div[data-baseweb="slider"] [role="slider"] { background: #0ea5e9 !important; border-color: #0ea5e9 !important; }

/* ── Download button (Standard) ── */
div[data-testid="stDownloadButton"] > button {
    background: #e0f2fe !important; color: #0284c7 !important; border: 1px solid #0ea5e9 !important; border-radius: 8px !important; font-size: 0.8rem !important; font-weight: 600 !important; width: 100% !important;
}
div[data-testid="stDownloadButton"] > button:hover { background: #0ea5e9 !important; color: #ffffff !important; }

/* ── Expander ── */
div[data-testid="stExpander"] { background: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 10px !important; }
div[data-testid="stExpander"] summary { color: #475569 !important; font-size: 0.82rem !important; }

/* ── Divider ── */
hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.5rem 0; }

/* ── Sidebar step ── */
.step { display:flex; align-items:flex-start; gap:0.7rem; margin-bottom:0.9rem; }
.step-n { background:#e0f2fe; color:#0284c7; font-size:0.65rem; font-weight:800; border-radius:5px; width:20px; height:20px; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px; }
.step-t { font-size:0.8rem; font-weight:600; color:#334155; }
.step-d { font-size:0.73rem; color:#64748b; margin-top:1px; line-height:1.45; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════
if not st.session_state.started:
    # Hide sidebar when on landing page
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none !important; }
    .block-container { max-width: 1200px !important; padding-top: 5rem !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="landing-container slide-up">
        <div class="landing-title">AnomalyIQ</div>
        <div class="landing-subtitle">AI-Powered Time-Series Anomaly Detection & Root Cause Analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Place button in the middle
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div class="slide-up" style="animation-delay: 0.2s;">', unsafe_allow_html=True)
        if st.button("Start Analysis", use_container_width=True, type="primary"):
            st.session_state.started = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.stop()


# ═══════════════════════════════════════════════════
# MAIN DASHBOARD (If started)
# ═══════════════════════════════════════════════════

# Apply fade-in to the main app container
st.markdown("""
<style>
.block-container { animation: fadeIn 0.6s ease-in-out forwards; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;
                    color:#0ea5e9;font-weight:700;margin-bottom:0.4rem;">AnomalyIQ</div>
        <div style="font-size:1.05rem;font-weight:800;color:#0f172a;letter-spacing:-0.03em;">
            Anomaly Detector</div>
        <div style="font-size:0.75rem;color:#64748b;margin-top:0.2rem;">Statistical Z-Score Engine</div>
    </div>
    <hr style="border-top:1px solid #e2e8f0;margin:0 0 1.3rem 0;">
    """, unsafe_allow_html=True)

    # Steps guide
    st.markdown("""
    <div style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;
                color:#64748b;font-weight:700;margin-bottom:0.8rem;">How to Use</div>
    <div class="step">
        <div class="step-n">1</div>
        <div><div class="step-t">Upload CSV</div>
        <div class="step-d">File with <code style="background:#f1f5f9;padding:1px 4px;border-radius:3px;color:#0284c7;font-size:0.7rem;">Date</code>
        and <code style="background:#f1f5f9;padding:1px 4px;border-radius:3px;color:#0284c7;font-size:0.7rem;">Value</code> columns</div></div>
    </div>
    <div class="step">
        <div class="step-n">2</div>
        <div><div class="step-t">Adjust Threshold</div>
        <div class="step-d">Control sensitivity — lower flags more anomalies</div></div>
    </div>
    <div class="step">
        <div class="step-n">3</div>
        <div><div class="step-t">Explore & Filter</div>
        <div class="step-d">Use interactive charts and date ranges</div></div>
    </div>
    <hr style="border-top:1px solid #e2e8f0;margin:1rem 0;">
    """, unsafe_allow_html=True)

    # Threshold slider
    st.markdown('<div style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#64748b;font-weight:700;margin-bottom:0.4rem;">Z-Score Threshold</div>', unsafe_allow_html=True)
    threshold = st.slider("threshold", min_value=1.0, max_value=4.0,
                          value=2.0, step=0.1, label_visibility="collapsed")
    st.markdown(f'<div style="font-size:0.7rem;color:#64748b;margin-top:0.2rem;">Flag rows where |Z| > <strong style="color:#0ea5e9;">{threshold:.1f}</strong></div>', unsafe_allow_html=True)

    st.markdown('<hr style="border-top:1px solid #e2e8f0;margin:1rem 0;">', unsafe_allow_html=True)
    show_rolling = st.toggle("Show 7-Day Rolling Average", value=True)
    st.markdown('<hr style="border-top:1px solid #e2e8f0;margin:1rem 0;">', unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#64748b;font-weight:700;margin-bottom:0.6rem;">Upload Data</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("upload", type=["csv"], label_visibility="collapsed")
    st.markdown('<div style="font-size:0.7rem;color:#64748b;margin-top:0.3rem;">CSV · <span style="color:#0ea5e9;">Date</span> + <span style="color:#0ea5e9;">Value</span> columns required</div>', unsafe_allow_html=True)


# ─── MAIN AREA ───
st.markdown("""
<div class="pg-header">
    <div class="pg-badge"><div class="pg-dot"></div>Sky Blue Edition</div>
    <h1>Anomaly Detection & <span>Root Cause Analyzer</span></h1>
    <p>Upload time-series CSV data to detect outliers, visualize patterns interactively, and understand root causes instantly.</p>
</div>
""", unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;">
        <div style="font-size:2.5rem;opacity:0.3;color:#0ea5e9;margin-bottom:1rem;">◈</div>
        <div style="font-size:1rem;font-weight:600;color:#0f172a;margin-bottom:0.4rem;">No data uploaded yet</div>
        <div style="font-size:0.82rem;color:#64748b;">Upload a CSV from the sidebar to begin.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Expected CSV Format</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        example = pd.DataFrame({
            "Date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "Value": [120, 115, 118, 950, 122],
        })
        st.dataframe(example, use_container_width=True, hide_index=True)
        st.markdown('<div style="font-size:0.72rem;color:#64748b;text-align:center;margin-top:0.4rem;">Row 4 would be flagged as an anomaly (spike)</div>', unsafe_allow_html=True)
    st.stop()

# Load & Validate
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
duplicate_rows = raw_df.duplicated().sum()

raw_df = raw_df.dropna(subset=["Date", "Value"]).reset_index(drop=True)

if raw_df.empty:
    st.error("No valid data rows remain after cleaning. Please check your file.")
    st.stop()

# Date range filter & Data Health
fc1, fc2, fc3 = st.columns([2, 2, 3])
date_min = raw_df["Date"].min().date()
date_max = raw_df["Date"].max().date()

with fc1:
    st.markdown('<div class="sec-label" style="margin-top:0.5rem;">Date Range Filter</div>', unsafe_allow_html=True)
    start_date = st.date_input("From", value=date_min, min_value=date_min, max_value=date_max)
with fc2:
    st.markdown('<div class="sec-label" style="margin-top:0.5rem; opacity:0;">Date</div>', unsafe_allow_html=True)
    end_date = st.date_input("To", value=date_max, min_value=date_min, max_value=date_max)
with fc3:
    st.markdown('<div class="sec-label" style="margin-top:0.5rem;">Data Health Snapshot</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:0.6rem 0.8rem; font-size:0.75rem; color:#475569; display:flex; gap:15px; flex-wrap:wrap;">
        <div>✅ <b>{len(raw_df):,}</b> Valid Rows</div>
        <div>⚠️ <b>{bad_rows}</b> Bad Rows (Skipped)</div>
        <div>🔄 <b>{duplicate_rows}</b> Duplicates</div>
    </div>
    """, unsafe_allow_html=True)

if start_date > end_date:
    st.error("'From' date must be before 'To' date.")
    st.stop()

df = raw_df[(raw_df["Date"].dt.date >= start_date) & (raw_df["Date"].dt.date <= end_date)].copy()
df = df.sort_values(by="Date").reset_index(drop=True)

if df.empty:
    st.warning("No data in selected date range. Adjust the filter above.")
    st.stop()

# Analysis
with st.spinner("Analyzing data..."):
    time.sleep(0.2)

    mean_val = df["Value"].mean()
    std_val  = df["Value"].std()
    min_val  = df["Value"].min()
    max_val  = df["Value"].max()
    
    if show_rolling:
        df["Rolling_Avg"] = df["Value"].rolling(window=7, min_periods=1).mean()

    if std_val == 0 or pd.isna(std_val):
        df["Z_Score"] = 0.0
    else:
        df["Z_Score"] = (df["Value"] - mean_val) / std_val

    df["Is_Anomaly"] = df["Z_Score"].abs() > threshold

    def get_reason(z):
        if z >  threshold: return "Spike"
        if z < -threshold: return "Drop"
        return "Normal"

    df["Type"] = df["Z_Score"].apply(get_reason)

anomalies_df    = df[df["Is_Anomaly"]].copy()
total_records   = len(df)
total_anomalies = int(df["Is_Anomaly"].sum())
anomaly_rate    = (total_anomalies / total_records * 100) if total_records else 0

st.markdown('<hr><div class="sec-label">Analysis Results</div><div class="sec-title">Summary Statistics</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="stat-grid">
    <div class="stat sky">
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
    <div class="stat indigo">
        <div class="stat-l">Std Deviation</div>
        <div class="stat-v">{std_val:,.1f}</div>
        <div class="stat-s">mean: {mean_val:,.1f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Interactive Chart
st.markdown('<hr><div class="sec-label">Interactive Visualization</div><div class="sec-title">Time Series — Anomalies Highlighted</div>', unsafe_allow_html=True)
col_chart, col_hist = st.columns([3, 1], gap="medium")

with col_chart:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["Value"], mode='lines', name='Value',
        line=dict(color='#0ea5e9', width=2), hovertemplate='<b>Date</b>: %{x}<br><b>Value</b>: %{y}<extra></extra>'
    ))
    if show_rolling:
        fig.add_trace(go.Scatter(
            x=df["Date"], y=df["Rolling_Avg"], mode='lines', name='7-Day Avg',
            line=dict(color='#94a3b8', width=2, dash='dot'), hoverinfo='skip'
        ))
    if not anomalies_df.empty:
        spikes = anomalies_df[anomalies_df["Type"] == "Spike"]
        drops = anomalies_df[anomalies_df["Type"] == "Drop"]
        if not spikes.empty:
            fig.add_trace(go.Scatter(
                x=spikes["Date"], y=spikes["Value"], mode='markers', name='Spike',
                marker=dict(color='#ef4444', size=10, line=dict(color='#fca5a5', width=2)),
                hovertemplate='<b>Date</b>: %{x}<br><b>Spike Value</b>: %{y}<br><b>Z-Score</b>: %{customdata:.2f}<extra></extra>',
                customdata=spikes["Z_Score"]
            ))
        if not drops.empty:
            fig.add_trace(go.Scatter(
                x=drops["Date"], y=drops["Value"], mode='markers', name='Drop',
                marker=dict(color='#6366f1', size=10, line=dict(color='#a5b4fc', width=2)),
                hovertemplate='<b>Date</b>: %{x}<br><b>Drop Value</b>: %{y}<br><b>Z-Score</b>: %{customdata:.2f}<extra></extra>',
                customdata=drops["Z_Score"]
            ))
            
    upper = mean_val + threshold * std_val
    lower = mean_val - threshold * std_val
    fig.add_hline(y=upper, line_dash="dash", line_color="#ef4444", line_width=1, annotation_text="Upper Bound", annotation_position="top left", annotation_font_size=10, annotation_font_color="#ef4444")
    fig.add_hline(y=lower, line_dash="dash", line_color="#6366f1", line_width=1, annotation_text="Lower Bound", annotation_position="bottom left", annotation_font_size=10, annotation_font_color="#6366f1")
    fig.add_hline(y=mean_val, line_dash="solid", line_color="#cbd5e1", line_width=1, annotation_text="Mean", annotation_position="top right", annotation_font_size=10, annotation_font_color="#64748b")

    fig.update_layout(
        plot_bgcolor="#f4f9fd", paper_bgcolor="#ffffff", margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=True, gridcolor="#e2e8f0", title="Date", title_font=dict(color="#64748b"), tickfont=dict(color="#64748b")),
        yaxis=dict(showgrid=True, gridcolor="#e2e8f0", title="Value", title_font=dict(color="#64748b"), tickfont=dict(color="#64748b")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color="#475569")), hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

with col_hist:
    fig_hist = go.Figure()
    normal_v = df.loc[~df["Is_Anomaly"], "Value"]
    anom_v   = df.loc[ df["Is_Anomaly"], "Value"]
    fig_hist.add_trace(go.Histogram(x=normal_v, name='Normal', marker_color='#0ea5e9', opacity=0.7, nbinsx=20))
    if len(anom_v):
        fig_hist.add_trace(go.Histogram(x=anom_v, name='Anomaly', marker_color='#ef4444', opacity=0.8, nbinsx=20))
    fig_hist.add_vline(x=mean_val, line_dash="dash", line_color="#f59e0b", line_width=2)
    fig_hist.update_layout(
        barmode='overlay', plot_bgcolor="#f4f9fd", paper_bgcolor="#ffffff", margin=dict(l=10, r=10, t=30, b=10),
        title=dict(text="Value Distribution", font=dict(size=14, color="#0f172a")),
        xaxis=dict(showgrid=False, title="Value", title_font=dict(size=11, color="#64748b"), tickfont=dict(size=10, color="#64748b")),
        yaxis=dict(showgrid=True, gridcolor="#e2e8f0", title="Count", title_font=dict(size=11, color="#64748b"), tickfont=dict(size=10, color="#64748b")), showlegend=False
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# Export / Table
st.markdown('<hr>', unsafe_allow_html=True)
tcol, dcol = st.columns([4, 1])
with tcol: st.markdown(f'<div class="sec-label">Flagged Records — {total_anomalies} anomalies</div>', unsafe_allow_html=True)
with dcol: st.markdown("<div style='height:0.1rem'></div>", unsafe_allow_html=True)

if total_anomalies > 0:
    show_df = anomalies_df[["Date", "Value", "Z_Score", "Type"]].copy()
    show_df["Date"]    = show_df["Date"].dt.strftime("%Y-%m-%d")
    show_df["Value"]   = show_df["Value"].round(2)
    show_df["Z_Score"] = show_df["Z_Score"].round(3)
    show_df.rename(columns={"Z_Score": "Z-Score", "Type": "Outlier Type"}, inplace=True)
    with dcol:
        st.download_button(label="⬇ Export Report CSV", data=show_df.to_csv(index=False).encode(), file_name="anomaly_report.csv", mime="text/csv", use_container_width=True)
    st.dataframe(show_df.reset_index(drop=True), use_container_width=True, height=min(350, 48 + 36 * total_anomalies))
else:
    st.markdown("""<div style="background:rgba(14,165,233,0.05);border:1px solid rgba(14,165,233,0.15);border-radius:10px;padding:1rem 1.3rem;font-size:0.84rem;color:#0284c7;">No anomalies detected at the current threshold — all values are statistically normal.</div>""", unsafe_allow_html=True)

with st.expander("View raw data (all rows)"):
    st.dataframe(df.head(200), use_container_width=True)

# Insights
st.markdown('<hr><div class="sec-label">Automated Insights</div><div class="sec-title">Root Cause Analysis</div>', unsafe_allow_html=True)
if total_anomalies == 0:
    st.markdown("""<div class="insight info"><div class="itag sky">Healthy</div><br><strong>No anomalies detected.</strong> The dataset is statistically stable.</div>""", unsafe_allow_html=True)
else:
    spk = anomalies_df[anomalies_df["Z_Score"] > 0]
    drp = anomalies_df[anomalies_df["Z_Score"] < 0]
    if not spk.empty:
        w = spk.loc[spk["Z_Score"].idxmax()]
        pct = ((w["Value"] - mean_val) / abs(mean_val)) * 100 if mean_val != 0 else 0
        st.markdown(f"""<div class="insight spike"><div class="itag rose">Spike · {len(spk)} event(s)</div><br><strong>{'Multiple spikes detected — ' if len(spk) > 1 else ''}Largest on {w['Date'].strftime('%Y-%m-%d')}</strong> — value hit <strong>{w['Value']:,.2f}</strong> ({pct:+.1f}% vs mean of {mean_val:,.1f}). Z-score: <strong>{w['Z_Score']:.2f}</strong>.</div>""", unsafe_allow_html=True)
    if not drp.empty:
        w = drp.loc[drp["Z_Score"].idxmin()]
        pct = ((w["Value"] - mean_val) / abs(mean_val)) * 100 if mean_val != 0 else 0
        st.markdown(f"""<div class="insight drop"><div class="itag indigo">Drop · {len(drp)} event(s)</div><br><strong>{'Multiple drops detected — ' if len(drp) > 1 else ''}Largest on {w['Date'].strftime('%Y-%m-%d')}</strong> — value fell to <strong>{w['Value']:,.2f}</strong> ({pct:+.1f}% vs mean of {mean_val:,.1f}). Z-score: <strong>{w['Z_Score']:.2f}</strong>.</div>""", unsafe_allow_html=True)
    if total_anomalies > 3:
        st.markdown(f"""<div class="insight warn"><div class="itag amber">Pattern</div><br><strong>Multiple anomalies observed</strong> — {total_anomalies} outliers across {total_records:,} records ({anomaly_rate:.1f}%). This may indicate a <strong>systematic issue</strong>.</div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="insight info"><div class="itag sky">Overview</div><br><strong>Dataset range:</strong> {min_val:,.1f} to {max_val:,.1f}. Mean: <strong>{mean_val:,.1f}</strong> · Std dev: <strong>{std_val:,.1f}</strong> · Threshold: <strong>±{threshold:.1f}σ</strong>. Period covers <strong>{(df['Date'].max() - df['Date'].min()).days + 1} days</strong>.</div>""", unsafe_allow_html=True)

st.markdown("<div style='height:2.5rem;'></div>", unsafe_allow_html=True)
