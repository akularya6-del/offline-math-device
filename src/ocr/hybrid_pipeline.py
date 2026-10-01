import cv2
import numpy as np
import pytesseract
import time
try:
    from PIL import Image
    from pix2tex.cli import LatexOCR
    math_ocr_model = LatexOCR()
except ImportError:
    math_ocr_model = None

class HybridOCR:
    def __init__(self):
        self.math_model = math_ocr_model

    def segment_image(self, img_cv):
        """Phase D: Automatic Text/Math Segmentation using heuristics"""
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        
        # Dilate heavily horizontally to form lines
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (100, 5))
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        regions = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if w > 20 and h > 10:
                # Math region heuristic: Centered, shorter width, or tall height (fractions/matrices)
                is_math = False
                if h > 40: # Tall (matrix/integral)
                    is_math = True
                elif w < (img_cv.shape[1] * 0.6) and x > (img_cv.shape[1] * 0.15): # Centered short block
                    is_math = True
                    
                regions.append({
                    'bbox': (x, y, x+w, y+h),
                    'type': 'math' if is_math else 'text'
                })
        
        regions.sort(key=lambda r: r['bbox'][1]) # Sort vertically
        return regions

    def process(self, img_cv):
        t_start = time.time()
        regions = self.segment_image(img_cv)
        
        results = []
        for r in regions:
            x1, y1, x2, y2 = r['bbox']
            # Add padding
            pad = 5
            x1, y1 = max(0, x1-pad), max(0, y1-pad)
            x2, y2 = min(img_cv.shape[1], x2+pad), min(img_cv.shape[0], y2+pad)
            crop = img_cv[y1:y2, x1:x2]
            
            if r['type'] == 'text':
                try:
                    text = pytesseract.image_to_string(crop, config='--psm 7').strip()
                    results.append({'type': 'text', 'content': text, 'bbox': (x1, y1, x2, y2)})
                except:
                    pass
            elif r['type'] == 'math':
                if self.math_model:
                    try:
                        crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
                        math_text = self.math_model(Image.fromarray(crop_rgb))
                        results.append({'type': 'math', 'content': math_text, 'bbox': (x1, y1, x2, y2)})
                    except Exception as e:
                        pass
                else:
                    try:
                        text = pytesseract.image_to_string(crop, config='--psm 7').strip()
                        results.append({'type': 'math', 'content': text, 'bbox': (x1, y1, x2, y2)})
                    except:
                        pass
                        
        latency = time.time() - t_start
        return results, latency
