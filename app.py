import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd
import time

from core_engine.violation_detector import ViolationDetector
from core_engine.lpr import LicensePlateRecognizer
from evidence_generator.annotator import EvidenceAnnotator

# Set page config FIRST
st.set_page_config(page_title="VeriTraf | Traffic AI", page_icon="🚨", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a professional dark mode / cyber look
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0E1117;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #E0E6ED;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Styled metrics */
    div[data-testid="stMetricValue"] {
        color: #00FF41;
        font-size: 2.5rem;
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        color: #8B949E;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        border: 1px solid rgba(240, 246, 252, 0.1);
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: 0.2s all;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2EA043;
        border-color: #8B949E;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 5px 5px 0px 0px;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
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

# Dashboard Header
st.markdown("<h1>🚨 VeriTraf <span style='color:#8B949E; font-size:1.5rem;'>| Enterprise Traffic Enforcement Edge</span></h1>", unsafe_allow_html=True)

# Generate Mock Historical Data for Analytics
@st.cache_data
def get_historical_data():
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30, freq='D')
    violations = np.random.randint(50, 200, size=30)
    # Add a spike
    violations[25] = 450
    return pd.DataFrame({'Date': dates, 'Violations Detected': violations}).set_index('Date')

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2088/2088090.png", width=60)
    st.markdown("## Control Panel")
    
    st.markdown("### Input Source")
    uploaded_file = st.file_uploader("Upload Surveillance Frame", type=['jpg', 'jpeg', 'png'])
    
    st.markdown("---")
    st.caption("System Status: 🟢 **ONLINE**")
    st.caption("Edge Node: `TRF-NODE-042`")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Live Inference", "📊 Global Analytics", "⚙️ Edge Configuration"])

# --- TAB 3: EDGE CONFIGURATION ---
with tab3:
    st.markdown("### ⚙️ Node Configuration Settings")
    st.markdown("Configure the AI detection parameters for this specific edge node.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Neural Engine")
        conf_threshold = st.slider("AI Confidence Threshold", 0.1, 1.0, 0.35, help="Minimum confidence score for the object detector.")
        run_lpr = st.toggle("Enable License Plate OCR", value=True)
        
    with col2:
        st.markdown("#### Geofencing (Illegal Parking)")
        st.markdown("Define a restricted horizontal zone (ROI) where parking is illegal.")
        enable_roi = st.toggle("Enable Restricted Zone (ROI)", value=False)
        roi_y_min, roi_y_max = st.slider("Restricted Zone (Y-axis bounds in pixels)", 0, 1000, (300, 500))

# --- TAB 1: LIVE INFERENCE ---
with tab1:
    if uploaded_file is not None:
        # Read Image
        image = Image.open(uploaded_file).convert('RGB')
        image_np = np.array(image)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Layout: Top Metrics (Initially empty)
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_placeholder1 = metric_col1.empty()
        metric_placeholder2 = metric_col2.empty()
        metric_placeholder3 = metric_col3.empty()
        
        metric_placeholder1.metric("Vehicles Tracked", "--")
        metric_placeholder2.metric("Violations Flagged", "--")
        metric_placeholder3.metric("Inference Time", "--")

        # Layout: Main Image Columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📷 Raw Surveillance Feed")
            
            # Preview ROI if enabled
            preview_img = image_np.copy()
            if enable_roi:
                h, w = preview_img.shape[:2]
                overlay = preview_img.copy()
                cv2.rectangle(overlay, (0, int(roi_y_min)), (w, int(roi_y_max)), (255, 0, 0), -1)
                cv2.addWeighted(overlay, 0.2, preview_img, 0.8, 0, preview_img)
            
            st.image(preview_img, width='stretch')
            analyze_btn = st.button("🚀 Execute AI Analysis")

        if analyze_btn:
            with st.spinner("Processing neural pipeline..."):
                start_time = time.time()
                
                # 1. Detect Violations
                roi = (roi_y_min, roi_y_max) if enable_roi else None
                analysis_results = detector.detect_violations(image_bgr, conf_threshold=conf_threshold, roi=roi)
                
                # 2. OCR
                if run_lpr:
                    for v in analysis_results['violations']:
                        v['lpr_text'] = lpr.extract_license_plate(image_bgr, v['box'])
                
                # 3. Annotate
                annotated_bgr, img_hash = annotator.annotate(image_bgr, analysis_results, roi=roi)
                annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)
                
                process_time = time.time() - start_time
                
                # Update Metrics
                total_vehicles = len(analysis_results['all_vehicles'])
                total_violations = len(analysis_results['violations'])
                
                metric_placeholder1.metric("Vehicles Tracked", total_vehicles)
                metric_placeholder2.metric("Violations Flagged", total_violations, delta=f"+{total_violations}" if total_violations > 0 else "0", delta_color="inverse")
                metric_placeholder3.metric("Inference Time", f"{process_time:.2f}s")

                with col2:
                    st.markdown("### 🎯 Verified Evidence Log")
                    st.image(annotated_rgb, width='stretch')
                    st.caption(f"🔒 **Cryptographic Hash (SHA-256):** `{img_hash}`")
                
                # Analytics Table & Download
                st.markdown("---")
                st.markdown("### 📑 Automated Incident Report")
                if total_violations > 0:
                    report_data = []
                    for v in analysis_results['violations']:
                        report_data.append({
                            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "Incident Type": "🚨 " + v['type'],
                            "Target Details": v.get('details', ''),
                            "AI Confidence": f"{float(v['conf'])*100:.1f}%",
                            "Extracted Plate": v.get('lpr_text', 'Not Requested')
                        })
                    df = pd.DataFrame(report_data)
                    
                    # Display beautifully using Streamlit's native dataframe config
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # CSV Download Button
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Secure Evidence (CSV)",
                        data=csv,
                        file_name=f'veritraf_report_{int(time.time())}.csv',
                        mime='text/csv',
                    )
                else:
                    st.success("✅ No violations detected in this frame. Compliance is 100%.")

    else:
        # Empty State Dashboard
        st.info("Awaiting visual input. Please upload a frame from the Control Panel.")
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Vehicles Tracked", "--")
        metric_col2.metric("Violations Flagged", "--")
        metric_col3.metric("Inference Time", "--")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📷 Raw Surveillance Feed")
            st.markdown("<div style='height: 300px; background-color: #161B22; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #8B949E; border: 1px dashed #30363D;'>STANDBY</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("### 🎯 Verified Evidence Log")
            st.markdown("<div style='height: 300px; background-color: #161B22; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #8B949E; border: 1px dashed #30363D;'>STANDBY</div>", unsafe_allow_html=True)

# --- TAB 2: GLOBAL ANALYTICS ---
with tab2:
    st.markdown("### 📊 Global Network Analytics")
    st.markdown("Historical data aggregated from all connected NeuroEdge nodes.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Violations Over Time (Last 30 Days)")
        historical_df = get_historical_data()
        st.area_chart(historical_df, color="#E63946")
        
    with col2:
        st.markdown("#### Violation Breakdown")
        breakdown_data = pd.DataFrame({
            "Violation Type": ["Speeding", "Triple Riding", "Illegal Parking", "Red Light", "Wrong Side"],
            "Count": [1240, 850, 2100, 430, 150]
        })
        st.bar_chart(breakdown_data.set_index("Violation Type"), color="#2EA043")
        
    st.markdown("---")
    st.markdown("#### Top Repeat Offenders")
    offenders = pd.DataFrame({
        "License Plate": ["KA-01-XX-9999", "MH-12-AB-1234", "DL-4C-NA-0001", "TN-09-XY-8888"],
        "Violations Flagged": [14, 9, 7, 5],
        "Last Detected Node": ["TRF-NODE-042", "TRF-NODE-011", "TRF-NODE-088", "TRF-NODE-042"]
    })
    st.dataframe(offenders, use_container_width=True, hide_index=True)
