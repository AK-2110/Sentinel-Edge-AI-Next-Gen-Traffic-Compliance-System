import cv2
import datetime
import hashlib
import numpy as np

class EvidenceAnnotator:
    def __init__(self):
        # Color palette for professional look
        self.COLOR_SAFE = (100, 255, 100) # Green
        self.COLOR_WARN = (0, 0, 255)     # Red
        self.COLOR_ROI = (0, 0, 200)      # Dark Red
        self.COLOR_TEXT = (255, 255, 255) # White

    def annotate(self, image_np: np.ndarray, analysis_results: dict, roi: tuple = None) -> tuple:
        """
        Draws professional bounding boxes and metadata on the image.
        Returns the annotated image and a cryptographic hash.
        """
        annotated_img = image_np.copy()
        
        # Draw ROI if provided
        if roi is not None:
            roi_y_min, roi_y_max = roi
            h, w = annotated_img.shape[:2]
            overlay = annotated_img.copy()
            cv2.rectangle(overlay, (0, int(roi_y_min)), (w, int(roi_y_max)), self.COLOR_ROI, -1)
            cv2.addWeighted(overlay, 0.25, annotated_img, 0.75, 0, annotated_img)
            
            # ROI Text banner
            cv2.rectangle(annotated_img, (0, int(roi_y_min)), (350, int(roi_y_min)+30), self.COLOR_ROI, -1)
            cv2.putText(annotated_img, "RESTRICTED ZONE (NO PARKING)", (10, int(roi_y_min) + 22), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.COLOR_TEXT, 2)

        # 1. Draw safe vehicles (translucent boxes to reduce clutter)
        for vehicle in analysis_results['all_vehicles']:
            box = vehicle['box']
            x1, y1, x2, y2 = map(int, box)
            
            # Skip if this vehicle is part of a violation (it will be drawn red later)
            is_violation = any(np.array_equal(v['box'], box) for v in analysis_results['violations'])
            if is_violation:
                continue
                
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), self.COLOR_SAFE, 1)
            
            if 'lpr_text' in vehicle and vehicle['lpr_text'] != "Not Detected":
                cv2.rectangle(annotated_img, (x1, y1-25), (x1+len(vehicle['lpr_text'])*15, y1), self.COLOR_SAFE, -1)
                cv2.putText(annotated_img, vehicle['lpr_text'], (x1+5, max(0, y1 - 8)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)

        # 2. Draw violations prominently
        for v in analysis_results['violations']:
            box = v['box']
            x1, y1, x2, y2 = map(int, box)
            
            # Thick red box
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), self.COLOR_WARN, 3)
            
            # Label background and text
            label = f"VIOLATION: {v['type']}"
            cv2.rectangle(annotated_img, (x1, y1-30), (x1+len(label)*12, y1), self.COLOR_WARN, -1)
            cv2.putText(annotated_img, label, (x1+5, max(0, y1 - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.COLOR_TEXT, 2)

        # 3. Enterprise Watermark and Timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        watermark_text = f"SENTINEL EVIDENCE | {timestamp}"
        
        cv2.rectangle(annotated_img, (0, 0), (len(watermark_text)*18, 40), (0,0,0), -1)
        cv2.putText(annotated_img, watermark_text, (10, 28), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Generate Hash for proof of integrity
        success, buffer = cv2.imencode('.jpg', annotated_img)
        img_hash = hashlib.sha256(buffer).hexdigest() if success else "HASH_FAILED"

        return annotated_img, img_hash

    def extract_evidence_card(self, image_np: np.ndarray, vehicle_box: list, padding: int = 50) -> np.ndarray:
        """
        Crops the specific vehicle out of the raw frame to create a zoomed-in evidence card.
        """
        h, w = image_np.shape[:2]
        x1, y1, x2, y2 = map(int, vehicle_box)
        
        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(w, x2 + padding)
        y2 = min(h, y2 + padding)
        
        return image_np[y1:y2, x1:x2].copy()
