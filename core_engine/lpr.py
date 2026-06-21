import easyocr
import cv2
import numpy as np

class LicensePlateRecognizer:
    def __init__(self):
        # Initialize EasyOCR for English
        # We only use gpu=False for compatibility on CPU setups, 
        # but change to True if running on a GPU.
        self.reader = easyocr.Reader(['en'], gpu=False)

    def extract_license_plate(self, image_np: np.ndarray, vehicle_box: list) -> str:
        """
        Given the original image and a vehicle bounding box,
        attempt to extract text from the lower portion of the vehicle.
        In a real scenario, a secondary YOLO model would detect the plate first.
        """
        try:
            x1, y1, x2, y2 = map(int, vehicle_box)
            
            # Ensure coordinates are within image bounds
            h, w = image_np.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            # We heuristic: plates are usually in the lower 30% of the bounding box
            crop_y1 = y1 + int((y2 - y1) * 0.7)
            vehicle_crop = image_np[crop_y1:y2, x1:x2]
            
            if vehicle_crop.size == 0:
                return "Not Detected"
            
            # --- Image Preprocessing for Better OCR ---
            # 1. Convert to grayscale
            gray = cv2.cvtColor(vehicle_crop, cv2.COLOR_BGR2GRAY)
            # 2. Resize to enlarge small characters
            gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            # 3. Apply bilateral filter to reduce noise while keeping edges sharp
            gray = cv2.bilateralFilter(gray, 11, 17, 17)
            # 4. Apply Otsu's thresholding
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Run EasyOCR on the preprocessed image
            results = self.reader.readtext(binary)
            
            extracted_text = []
            for (bbox, text, prob) in results:
                # Filter out very low confidence
                if prob > 0.3:
                    extracted_text.append(text.upper())
            
            return " ".join(extracted_text) if extracted_text else "Not Detected"
        except Exception as e:
            print(f"OCR Error: {e}")
            return "Not Detected"
