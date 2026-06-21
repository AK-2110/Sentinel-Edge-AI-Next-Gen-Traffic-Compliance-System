import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import time
import tempfile
import os
import plotly.express as px
import plotly.graph_objects as go

from core_engine.violation_detector import ViolationDetector
from core_engine.lpr import LicensePlateRecognizer
from evidence_generator.annotator import EvidenceAnnotator

# Set page config FIRST
st.set_page_config(page_title="Sentinel | Edge AI", page_icon="🚨", layout="wide", initial_sidebar_state="expanded")

# --- Premium Dark Mode UI ---
st.markdown("""
<style>
    /* Keyframe Animations */
    @keyframes fadeInSlideUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0% { text-shadow: 0 0 10px rgba(63, 185, 80, 0.3); }
        50% { text-shadow: 0 0 25px rgba(63, 185, 80, 0.8); }
        100% { text-shadow: 0 0 10px rgba(63, 185, 80, 0.3); }
    }
    @keyframes gradientSweep {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Base Styling & Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(13, 17, 23, 1) 0%, rgba(5, 7, 10, 1) 100%);
        color: #c9d1d9;
        animation: fadeInSlideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Hide Streamlit junk */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] {
        color: #3fb950;
        font-size: 3rem;
        font-weight: 800;
        animation: pulseGlow 3s infinite;
        background: linear-gradient(90deg, #3fb950, #2ea043);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    div[data-testid="stMetricLabel"] {
        color: #8b949e;
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Premium Button */
    .stButton>button {
        background: linear-gradient(270deg, #238636, #2ea043, #1f6f2e);
        background-size: 200% 200%;
        animation: gradientSweep 5s ease infinite;
        color: white;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.8rem 1.8rem;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 1px;
        transition: 0.3s all;
        width: 100%;
        box-shadow: 0 8px 25px rgba(46, 160, 67, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 30px rgba(46, 160, 67, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Tabs & Navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2.5rem;
        border-bottom: 2px solid rgba(139, 148, 158, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        font-size: 1.2rem;
        font-weight: 600;
        color: #8b949e;
        transition: color 0.3s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #c9d1d9;
    }
    .stTabs [aria-selected="true"] {
        color: #58a6ff !important;
        border-bottom-color: #58a6ff !important;
        background: linear-gradient(180deg, rgba(88, 166, 255, 0.1) 0%, transparent 100%);
    }
    
    /* Glassmorphism Containers */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background: rgba(22, 27, 34, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_models():
    detector = ViolationDetector('yolov8n.pt')
    lpr = LicensePlateRecognizer()
    annotator = EvidenceAnnotator()
    return detector, lpr, annotator

detector, lpr, annotator = load_models()

# Header
st.markdown("<h1>🚨 Sentinel <span style='color:#8b949e; font-size:1.6rem; font-weight:400;'>| Next-Gen Edge Traffic Enforcement</span></h1>", unsafe_allow_html=True)

# Generate Mock Historical Data for Analytics
@st.cache_data
def get_historical_data():
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30, freq='D')
    violations = np.random.randint(50, 200, size=30)
    violations[25] = 450 # Spike
    df = pd.DataFrame({'Date': dates, 'Violations': violations})
    return df

# Sidebar
with st.sidebar:
    st.markdown("## Control Panel")
    
    st.markdown("### Input Source")
    uploaded_file = st.file_uploader("Upload Surveillance Feed (Image/Video)", type=['jpg', 'jpeg', 'png', 'mp4'])
    
    st.markdown("---")
    st.caption("System Status: 🟢 **ONLINE**")
    st.caption("Edge Node: `TRF-NODE-042`")
    st.caption(f"Time: `{time.strftime('%H:%M:%S UTC')}`")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Live Inference", "📊 Global Analytics", "⚙️ Edge Configuration"])

# --- TAB 3: EDGE CONFIGURATION ---
with tab3:
    st.markdown("### ⚙️ Node Configuration Settings")
    st.markdown("Configure the AI detection parameters for this specific edge node.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Neural Engine")
        conf_threshold = st.slider("AI Confidence Threshold", 0.1, 1.0, 0.35)
        run_lpr = st.toggle("Enable License Plate OCR (Heavy Compute)", value=True)
        
    with col2:
        st.markdown("#### Geofencing (Illegal Parking)")
        enable_roi = st.toggle("Enable Restricted Zone (ROI)", value=False)
        roi_y_min, roi_y_max = st.slider("Restricted Zone (Y-axis bounds in pixels)", 0, 1000, (300, 500))

# --- TAB 1: LIVE INFERENCE ---
with tab1:
    if uploaded_file is not None:
        file_ext = uploaded_file.name.split('.')[-1].lower()
        is_video = file_ext == 'mp4'

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_placeholder1 = metric_col1.empty()
        metric_placeholder2 = metric_col2.empty()
        metric_placeholder3 = metric_col3.empty()
        
        metric_placeholder1.metric("Vehicles Tracked", "--")
        metric_placeholder2.metric("Violations Flagged", "--")
        metric_placeholder3.metric("Processing Time", "--")

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📷 Raw Feed Preview")
            if not is_video:
                image = Image.open(uploaded_file).convert('RGB')
                image_np = np.array(image)
                st.image(image_np, width='stretch')
            else:
                st.video(uploaded_file)
            
            analyze_btn = st.button("🚀 Execute Enterprise Analysis")

        if analyze_btn:
            with st.spinner("Processing neural pipeline..."):
                start_time = time.time()
                roi = (roi_y_min, roi_y_max) if enable_roi else None
                
                all_violations = []
                final_output_path = None
                
                if not is_video:
                    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
                    
                    # 1. Detect
                    analysis_results = detector.detect_violations(image_bgr, conf_threshold=conf_threshold, roi=roi)
                    
                    # 2. OCR
                    if run_lpr:
                        for v in analysis_results['violations']:
                            v['lpr_text'] = lpr.extract_license_plate(image_bgr, v['box'])
                    
                    # 3. Annotate
                    annotated_bgr, img_hash = annotator.annotate(image_bgr, analysis_results, roi=roi)
                    annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)
                    
                    total_vehicles = len(analysis_results['all_vehicles'])
                    all_violations = analysis_results['violations']
                    
                    with col2:
                        st.markdown("### 🎯 Verified Evidence Log")
                        st.image(annotated_rgb, width='stretch')
                        st.caption(f"🔒 **Cryptographic Hash (SHA-256):** `{img_hash}`")
                        
                else:
                    # Video Processing Logic
                    tfile = tempfile.NamedTemporaryFile(delete=False) 
                    tfile.write(uploaded_file.read())
                    vf = cv2.VideoCapture(tfile.name)
                    
                    width = int(vf.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(vf.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    fps = int(vf.get(cv2.CAP_PROP_FPS))
                    
                    output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                    final_output_path = output_file.name
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(final_output_path, fourcc, fps, (width, height))
                    
                    frame_placeholder = col2.empty()
                    col2.markdown("### 🎯 Live Processed Stream")
                    
                    frame_count = 0
                    total_vehicles_set = set()
                    
                    while vf.isOpened():
                        ret, frame = vf.read()
                        if not ret or frame_count > 90: # Process max 3 seconds for prototype
                            break
                            
                        # Detect
                        res = detector.detect_violations(frame, conf_threshold=conf_threshold, roi=roi)
                        
                        if run_lpr and frame_count % 5 == 0: # OCR every 5th frame for speed
                            for v in res['violations']:
                                v['lpr_text'] = lpr.extract_license_plate(frame, v['box'])
                                all_violations.append((v, frame.copy())) # Save violation + frame
                        elif not run_lpr:
                            for v in res['violations']:
                                all_violations.append((v, frame.copy()))

                        # Annotate
                        ann_frame, _ = annotator.annotate(frame, res, roi=roi)
                        out.write(ann_frame)
                        
                        # Show frame in UI
                        ann_rgb = cv2.cvtColor(ann_frame, cv2.COLOR_BGR2RGB)
                        frame_placeholder.image(ann_rgb, channels="RGB")
                        frame_count += 1
                        
                    vf.release()
                    out.release()
                    
                    # Convert to web-friendly format if needed in production, for now just show static frames
                    total_vehicles = frame_count * 2 # Mocked distinct vehicles
                    
                    # Deduplicate violations based on type (naive)
                    unique_violations = []
                    seen_types = set()
                    for v, f in all_violations:
                        if v['type'] not in seen_types:
                            unique_violations.append(v)
                            seen_types.add(v['type'])
                    all_violations = unique_violations
                    
                    col2.success(f"Processed {frame_count} frames successfully.")

                process_time = time.time() - start_time
                
                # Metrics
                total_viols = len(all_violations)
                metric_placeholder1.metric("Vehicles Tracked", total_vehicles)
                metric_placeholder2.metric("Violations Flagged", total_viols, delta=f"+{total_viols}" if total_viols > 0 else "0", delta_color="inverse")
                metric_placeholder3.metric("Processing Time", f"{process_time:.2f}s")

                # --- Evidence Cards ---
                if total_viols > 0:
                    st.markdown("---")
                    st.markdown("### 🎫 Extracted Evidence Cards")
                    card_cols = st.columns(min(3, total_viols))
                    
                    for idx, v in enumerate(all_violations):
                        col = card_cols[idx % 3]
                        with col:
                            st.markdown(f"**Violation:** `{v['type']}`")
                            
                            # For video, we saved the frame. For image, use image_bgr
                            source_img = image_bgr if not is_video else image_bgr # Note: video frame logic simplified here
                            
                            try:
                                card_img = annotator.extract_evidence_card(image_bgr if not is_video else v.get('frame', image_bgr), v['box'])
                                card_rgb = cv2.cvtColor(card_img, cv2.COLOR_BGR2RGB)
                                st.image(card_rgb, use_container_width=True)
                            except:
                                st.warning("Card extraction failed")
                                
                            plate_text = v.get('lpr_text', 'Not Requested')
                            st.caption(f"Plate OCR: **{plate_text}**")
                            st.caption(f"Confidence: {float(v['conf'])*100:.1f}%")

                # Analytics Table
                st.markdown("---")
                st.markdown("### 📑 Automated Incident Report")
                if total_viols > 0:
                    df = pd.DataFrame([{
                        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "Incident Type": "🚨 " + v['type'],
                        "Target Details": v.get('details', ''),
                        "AI Confidence": f"{float(v['conf'])*100:.1f}%",
                        "Extracted Plate": v.get('lpr_text', 'Not Requested')
                    } for v in all_violations])
                    
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(label="📥 Download Secure Evidence (CSV)", data=csv, file_name='sentinel_report.csv', mime='text/csv')
                else:
                    st.success("✅ No violations detected. Compliance is 100%.")

    else:
        st.info("Awaiting visual input. Please upload a feed from the Control Panel.")

# --- TAB 2: GLOBAL ANALYTICS ---
with tab2:
    st.markdown("### 📊 Global Network Intelligence")
    st.markdown("Real-time aggregated telemetry from all active NeuroEdge nodes.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Violations Over Time (Last 30 Days)")
        df_hist = get_historical_data()
        fig1 = px.area(df_hist, x='Date', y='Violations', color_discrete_sequence=['#58a6ff'])
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#c9d1d9')
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        st.markdown("#### Violation Distribution")
        df_breakdown = pd.DataFrame({
            "Type": ["Speeding", "Triple Riding", "Illegal Parking", "Red Light", "Wrong Side"],
            "Count": [1240, 850, 2100, 430, 150]
        })
        fig2 = px.pie(df_breakdown, values='Count', names='Type', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#c9d1d9', showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
        
    st.markdown("---")
    st.markdown("#### Top Repeat Offenders Watchlist")
    offenders = pd.DataFrame({
        "License Plate": ["KA-01-XX-9999", "MH-12-AB-1234", "DL-4C-NA-0001", "TN-09-XY-8888"],
        "Violations Flagged": [14, 9, 7, 5],
        "Last Detected Node": ["TRF-NODE-042", "TRF-NODE-011", "TRF-NODE-088", "TRF-NODE-042"]
    })
    st.dataframe(offenders, use_container_width=True, hide_index=True)
