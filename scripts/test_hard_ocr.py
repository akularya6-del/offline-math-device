import os
import time
import pytesseract
import cv2
import json

data_dir = "../data/hard_ocr_benchmark"

def test_hard_ocr():
    images = sorted([f for f in os.listdir(data_dir) if f.endswith('.png')])
    results = []
    
    for img_file in images:
        img_path = os.path.join(data_dir, img_file)
        img = cv2.imread(img_path)
        
        # Test Tesseract (Standard OCR)
        try:
            text_tess = pytesseract.image_to_string(img, config='--psm 7').strip()
        except Exception as e:
            text_tess = "ERROR"
            
        # Mock pix2tex (Math OCR) for now if not available
        # Real pix2tex would be called here: `model(img)`
        
        results.append({
            "file": img_file,
            "tesseract_output": text_tess,
            "math_ocr_output": "PENDING"
        })
        
    for r in results:
        print(f"File: {r['file']}")
        print(f"Tesseract: {r['tesseract_output']}\n")
        
if __name__ == "__main__":
    test_hard_ocr()
