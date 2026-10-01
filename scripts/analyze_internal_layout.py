import cv2
import os
import json
import time
import numpy as np

crop_dir = "data/real_cuet/question_crops"
debug_dir = "reports/question_detection_debug"

def analyze_internal_layout(q_id, img_path):
    img = cv2.imread(img_path)
    if img is None: return
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    # 1. Text Regions: wide horizontal dilation to find lines
    kernel_text = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 3))
    dilated_text = cv2.dilate(thresh, kernel_text, iterations=1)
    
    contours_text, _ = cv2.findContours(dilated_text, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    text_boxes = []
    math_boxes = []
    
    for c in contours_text:
        x, y, w, h = cv2.boundingRect(c)
        if w < 20 or h < 10: continue
        
        # Heuristics:
        # If it's very tall compared to normal text (h > 45), it's likely a matrix or integral block
        # If it's heavily indented (x > 300) and short width, it might be a standalone equation
        
        if h > 45 or (x > 300 and w < img.shape[1]*0.6):
            math_boxes.append([x, y, x+w, y+h])
        else:
            text_boxes.append([x, y, x+w, y+h])
            
    # Draw debugs
    debug_text = img.copy()
    for b in text_boxes:
        cv2.rectangle(debug_text, (b[0], b[1]), (b[2], b[3]), (255, 0, 0), 2)
        
    debug_math = img.copy()
    for b in math_boxes:
        cv2.rectangle(debug_math, (b[0], b[1]), (b[2], b[3]), (0, 0, 255), 2)
        
    cv2.imwrite(os.path.join(debug_dir, f"{q_id}_text_regions.png"), debug_text)
    cv2.imwrite(os.path.join(debug_dir, f"{q_id}_math_regions.png"), debug_math)
    
if __name__ == "__main__":
    with open(os.path.join(crop_dir, "question_boxes.json"), "r") as f:
        questions = json.load(f)
        
    for q in questions:
        print(f"Analyzing internal layout for {q['id']}...")
        analyze_internal_layout(q["id"], q["crop_path"])
        
    print("Internal layout analysis complete.")
