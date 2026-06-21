from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import cv2
import numpy as np
import base64
import time

from core_engine.violation_detector import ViolationDetector
from core_engine.lpr import LicensePlateRecognizer
from evidence_generator.annotator import EvidenceAnnotator

app = FastAPI(title="Sentinel Edge AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load AI models once on startup
detector = ViolationDetector('yolov8n.pt')
lpr = LicensePlateRecognizer()
annotator = EvidenceAnnotator()

def encode_image(img_np):
    success, buffer = cv2.imencode('.jpg', img_np)
    if success:
        return base64.b64encode(buffer).decode('utf-8')
    return ""

@app.post("/analyze")
async def analyze_frame(
    file: UploadFile = File(...), 
    conf_threshold: float = Form(0.35), 
    run_lpr: bool = Form(True)
):
    start_time = time.time()
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image_bgr is None:
        return {"error": "Invalid image format"}
        
    # 1. Detect
    analysis_results = detector.detect_violations(image_bgr, conf_threshold=conf_threshold, roi=None)
    
    # 2. OCR
    if run_lpr:
        for v in analysis_results['violations']:
            v['lpr_text'] = lpr.extract_license_plate(image_bgr, v['box'])
            
    # 3. Annotate full frame
    annotated_bgr, img_hash = annotator.annotate(image_bgr, analysis_results, roi=None)
    
    # 4. Extract Evidence Cards
    evidence_cards = []
    for v in analysis_results['violations']:
        try:
            card_img = annotator.extract_evidence_card(image_bgr, v['box'])
            evidence_cards.append({
                "type": v['type'],
                "conf": float(v['conf']),
                "details": v.get('details', ''),
                "lpr_text": v.get('lpr_text', 'Not Requested'),
                "image_b64": encode_image(card_img)
            })
        except Exception as e:
            print(f"Error extracting card: {e}")

    # Convert numpy types to native Python types for JSON serialization
    for v in analysis_results['violations']:
        v['box'] = [float(x) for x in v['box']]
        v['conf'] = float(v['conf'])
    for v in analysis_results['all_vehicles']:
        v['box'] = [float(x) for x in v['box']]
        v['conf'] = float(v['conf'])
            
    process_time = time.time() - start_time
    
    return {
        "status": "success",
        "process_time": round(process_time, 2),
        "total_vehicles": len(analysis_results['all_vehicles']),
        "total_violations": len(analysis_results['violations']),
        "hash": img_hash,
        "annotated_frame_b64": encode_image(annotated_bgr),
        "evidence_cards": evidence_cards,
        "violations": analysis_results['violations']
    }

if __name__ == "__main__":
    uvicorn.run("backend_api:app", host="0.0.0.0", port=8000, reload=True)
