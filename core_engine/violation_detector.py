import cv2
import numpy as np
import random
from ultralytics import YOLO
from typing import Dict, List, Any

class ViolationDetector:
    def __init__(self, model_path: str = 'yolov8n.pt'):
        """
        Initializes the YOLO model and defines target classes.
        """
        try:
            self.model = YOLO(model_path)
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            raise e
        
        # COCO Classes we care about
        self.PERSON_CLASS = 0
        self.MOTORCYCLE_CLASS = 3
        self.CAR_CLASS = 2
        self.BUS_CLASS = 5
        self.TRUCK_CLASS = 7

    def detect_violations(self, image_np: np.ndarray, conf_threshold: float = 0.3, roi: tuple = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Detects vehicles and evaluates violations such as Triple Riding and Illegal Parking.
        Adds mock Speeding detection for prototype demonstration.
        """
        try:
            results = self.model(image_np, conf=conf_threshold)[0]
        except Exception as e:
            print(f"Inference error: {e}")
            return {'violations': [], 'all_vehicles': [], 'all_persons': []}
        
        boxes = results.boxes.xyxy.cpu().numpy()
        classes = results.boxes.cls.cpu().numpy()
        confidences = results.boxes.conf.cpu().numpy()
        
        persons = []
        motorcycles = []
        other_vehicles = []
        
        for box, cls, conf in zip(boxes, classes, confidences):
            item = {'box': box, 'conf': float(conf), 'cls': int(cls)}
            if cls == self.PERSON_CLASS:
                persons.append(item)
            elif cls == self.MOTORCYCLE_CLASS:
                motorcycles.append(item)
            elif cls in [self.CAR_CLASS, self.BUS_CLASS, self.TRUCK_CLASS]:
                other_vehicles.append(item)

        violations = []
        
        # 1. Check for Triple Riding
        for moto in motorcycles:
            moto_box = moto['box']
            riders_on_this_moto = 0
            for person in persons:
                person_box = person['box']
                if self._check_overlap(moto_box, person_box):
                    riders_on_this_moto += 1
            
            if riders_on_this_moto > 2:
                violations.append({
                    'type': 'Triple Riding',
                    'box': moto_box,
                    'conf': moto['conf'],
                    'details': f'{riders_on_this_moto} persons detected on one motorcycle'
                })
        
        # 2. Check for Illegal Parking in ROI
        if roi is not None:
            roi_y_min, roi_y_max = roi
            for vehicle in other_vehicles:
                box = vehicle['box']
                # Check if bottom-center of the vehicle is in the ROI
                center_x = (box[0] + box[2]) / 2
                bottom_y = box[3]
                
                if roi_y_min <= bottom_y <= roi_y_max:
                    violations.append({
                        'type': 'Illegal Parking / Zone',
                        'box': box,
                        'conf': vehicle['conf'],
                        'details': 'Vehicle detected inside restricted zone'
                    })

        # 3. MOCK Speed Radar for Demo Purposes
        # In a real app, speed is derived from optical flow or radar integration.
        for vehicle in other_vehicles:
            if random.random() < 0.15: # 15% chance to simulate a speeding vehicle
                simulated_speed = random.randint(85, 120)
                violations.append({
                    'type': 'Speeding',
                    'box': vehicle['box'],
                    'conf': vehicle['conf'],
                    'details': f'Simulated radar detected {simulated_speed} km/h (Limit: 80 km/h)'
                })
        
        return {
            'violations': violations,
            'all_vehicles': motorcycles + other_vehicles,
            'all_persons': persons
        }

    def _check_overlap(self, box1: list, box2: list) -> bool:
        """
        Checks if person box (box2) overlaps significantly with motorcycle box (box1).
        """
        x1_inter = max(box1[0], box2[0])
        y1_inter = max(box1[1], box2[1])
        x2_inter = min(box1[2], box2[2])
        y2_inter = min(box1[3], box2[3])
        
        inter_area = max(0, x2_inter - x1_inter) * max(0, y2_inter - y1_inter)
        if inter_area > 0:
            person_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
            # If intersection is more than 30% of person's area, assume riding
            if person_area > 0 and (inter_area / person_area) > 0.3:
                return True
        return False
