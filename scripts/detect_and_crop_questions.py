import cv2
import os
import json
import numpy as np

page_dir = "data/real_cuet/pages"
out_dir = "data/real_cuet/question_crops"
debug_dir = "reports/real_cuet_debug"
os.makedirs(out_dir, exist_ok=True)
os.makedirs(debug_dir, exist_ok=True)

def detect_questions(page_path, page_num):
    img = cv2.imread(page_path)
    if img is None:
        print(f"Failed to load {page_path}")
        return []
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    kernel_lines = cv2.getStructuringElement(cv2.MORPH_RECT, (200, 10))
    dilated_lines = cv2.dilate(thresh, kernel_lines, iterations=1)
    contours, _ = cv2.findContours(dilated_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    boxes = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > 100 and h > 10:
            boxes.append([x, y, x+w, y+h])
            
    if not boxes: return []
    
    boxes = sorted(boxes, key=lambda b: b[1])
    merged = []
    current = list(boxes[0])
    
    for b in boxes[1:]:
        if b[1] - current[3] < 80:
            current[0] = min(current[0], b[0])
            current[1] = min(current[1], b[1])
            current[2] = max(current[2], b[2])
            current[3] = max(current[3], b[3])
        else:
            merged.append(current)
            current = list(b)
    merged.append(current)
        
    debug_img = img.copy()
    questions = []
    
    for i, b in enumerate(merged):
        if (b[3] - b[1]) > 50:
            pad = 10
            x1 = max(0, b[0] - pad)
            y1 = max(0, b[1] - pad)
            x2 = min(img.shape[1], b[2] + pad)
            y2 = min(img.shape[0], b[3] + pad)
            
            cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            crop = img[y1:y2, x1:x2]
            
            q_id = f"P{page_num:02d}_Q{i+1:02d}"
            crop_path = os.path.join(out_dir, f"{q_id}.png")
            cv2.imwrite(crop_path, crop)
            
            questions.append({
                "id": q_id,
                "page": page_num,
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "crop_path": crop_path
            })
            
    cv2.imwrite(os.path.join(debug_dir, f"page_{page_num:02d}_detected.png"), debug_img)
    return questions

if __name__ == "__main__":
    all_questions = []
    pages = sorted([p for p in os.listdir(page_dir) if p.endswith('.png')])
    for i, page_file in enumerate(pages):
        page_path = os.path.join(page_dir, page_file)
        qs = detect_questions(page_path, i+1)
        print(f"Page {i+1}: {len(qs)} questions detected")
        all_questions.extend(qs)
        
    with open(os.path.join(out_dir, "question_boxes.json"), "w") as f:
        json.dump(all_questions, f, indent=4)
