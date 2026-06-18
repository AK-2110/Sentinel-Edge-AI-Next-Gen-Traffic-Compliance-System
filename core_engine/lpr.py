import easyocr
import cv2
import numpy as np

class LicensePlateRecognizer:
    def __init__(self):
        # Initialize EasyOCR for English
        # We only use gpu=False for compatibility on CPU setups, 
        # but change to True if running on a GPU.
        self.reader = easyocr.Reader(['en'], gpu=False)

    def extract_license_plate(self, image_np, vehicle_box):
        """
        Given the original image and a vehicle bounding box,
        attempt to extract text from the lower portion of the vehicle.
        In a real scenario, a secondary YOLO model would detect the plate first.
        """
        x1, y1, x2, y2 = map(int, vehicle_box)
        
        # Ensure coordinates are within image bounds
        h, w = image_np.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        # We heuristic: plates are usually in the lower 30% of the bounding box
        crop_y1 = y1 + int((y2 - y1) * 0.7)
        vehicle_crop = image_np[crop_y1:y2, x1:x2]
        
        if vehicle_crop.size == 0:
            return None
        
        # Convert to grayscale to improve OCR
        gray = cv2.cvtColor(vehicle_crop, cv2.COLOR_BGR2GRAY)
        
        # Run EasyOCR
        results = self.reader.readtext(gray)
        
        extracted_text = []
        for (bbox, text, prob) in results:
            # Filter out very low confidence
            if prob > 0.3:
                extracted_text.append(text)
        
        return " ".join(extracted_text) if extracted_text else "Not Detected"
