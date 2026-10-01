import cv2
import numpy as np

class HybridOCR:
    def __init__(self, text_ocr_model, math_ocr_model):
        self.text_ocr = text_ocr_model
        self.math_ocr = math_ocr_model
        
    def extract_regions(self, img_cv):
        """
        Uses OpenCV contours to separate text lines from standalone math equations.
        Real implementation would use YOLO/RT-DETR.
        """
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Dilate horizontally to connect text words into lines
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 5))
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        regions = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w > 10 and h > 10:
                regions.append({"bbox": (x, y, w, h), "type": "unknown"})
                
        # Sort vertically
        regions.sort(key=lambda r: r["bbox"][1])
        
        # Naive classifier: If it's tall and centered, it's probably math. Else text.
        for r in regions:
            x, y, w, h = r["bbox"]
            if h > 40 and w < img_cv.shape[1] * 0.8:
                r["type"] = "math"
            else:
                r["type"] = "text"
                
        return regions

    def process(self, img_path):
        img_cv = cv2.imread(img_path)
        regions = self.extract_regions(img_cv)
        
        reconstructed = {
            "text": [],
            "math": []
        }
        
        for r in regions:
            x, y, w, h = r["bbox"]
            roi = img_cv[y:y+h, x:x+w]
            
            if r["type"] == "text":
                # text_out = self.text_ocr(roi)
                reconstructed["text"].append("TEXT_REGION")
            else:
                # math_out = self.math_ocr(roi)
                reconstructed["math"].append("MATH_REGION")
                
        return reconstructed
