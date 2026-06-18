import cv2
import datetime
import hashlib

class EvidenceAnnotator:
    def __init__(self):
        pass

    def annotate(self, image_np, analysis_results, roi=None):
        """
        Draws bounding boxes and metadata on the image.
        Returns the annotated image and a cryptographic hash.
        """
        annotated_img = image_np.copy()
        
        # Draw ROI if provided
        if roi is not None:
            roi_y_min, roi_y_max = roi
            h, w = annotated_img.shape[:2]
            # Draw a semi-transparent red overlay for the restricted zone
            overlay = annotated_img.copy()
            cv2.rectangle(overlay, (0, int(roi_y_min)), (w, int(roi_y_max)), (0, 0, 255), -1)
            cv2.addWeighted(overlay, 0.2, annotated_img, 0.8, 0, annotated_img)
            cv2.putText(annotated_img, "RESTRICTED ZONE (NO PARKING)", (10, int(roi_y_min) + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        
        # Draw all vehicles in green
        for vehicle in analysis_results['all_vehicles']:
            box = vehicle['box']
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Add LPR if available
            if 'lpr_text' in vehicle and vehicle['lpr_text'] != "Not Detected":
                cv2.putText(annotated_img, vehicle['lpr_text'], (x1, max(0, y1 - 10)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Draw violations in red
        for v in analysis_results['violations']:
            box = v['box']
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            
            label = f"VIOLATION: {v['type']}"
            cv2.putText(annotated_img, label, (x1, max(0, y1 - 10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Add Watermark and Timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        watermark_text = f"EVIDENCE GENERATED: {timestamp}"
        cv2.putText(annotated_img, watermark_text, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Generate Hash for proof of integrity
        success, buffer = cv2.imencode('.jpg', annotated_img)
        img_hash = hashlib.sha256(buffer).hexdigest() if success else "HASH_FAILED"

        return annotated_img, img_hash
