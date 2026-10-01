import os
import json
import time
import cv2
import pytesseract

try:
    from PIL import Image
    from pix2tex.cli import LatexOCR
    has_pix2tex = True
except ImportError:
    has_pix2tex = False

data_dir = "../data/benchmark_500"
gt_file = os.path.join(data_dir, "ground_truth.json")

def evaluate_string(pred, target):
    """Basic string distance metric (token accuracy)."""
    # Remove spaces and formatting for structural comparison
    pred_clean = pred.replace(" ", "").replace("\n", "").strip()
    target_clean = target.replace(" ", "").replace("\n", "").strip()
    if not target_clean: return 1.0
    
    # Very crude accuracy: exact match
    return 1.0 if pred_clean == target_clean else 0.0

def run_benchmark():
    with open(gt_file, 'r') as f:
        dataset = json.load(f)
        
    print(f"Loaded {len(dataset)} questions for benchmarking.")
    
    # Initialize models
    if has_pix2tex:
        print("Initializing LatexOCR (pix2tex)...")
        math_model = LatexOCR()
    else:
        print("pix2tex not found. Mocking math model.")
        math_model = None

    results = []
    
    # Benchmark stats
    tess_correct = 0
    math_correct = 0
    tess_time = 0
    math_time = 0
    
    # Test a subset to save time if needed, e.g. 50 images
    subset = dataset[:50]
    
    print("Running inference...")
    for idx, item in enumerate(subset):
        img_path = item["image"]
        if not os.path.exists(img_path):
            continue
            
        img_cv2 = cv2.imread(img_path)
        img_pil = Image.open(img_path).convert('RGB')
        
        # 1. Standard OCR (Tesseract)
        t0 = time.time()
        try:
            tess_text = pytesseract.image_to_string(img_cv2, config='--psm 6').strip()
        except:
            tess_text = ""
        tess_time += (time.time() - t0)
        
        # 2. Math OCR (pix2tex)
        t0 = time.time()
        if has_pix2tex:
            try:
                # pix2tex works best on pure equations, not full text pages.
                # When fed a full page, it will try to transcribe EVERYTHING as LaTeX.
                math_text = math_model(img_pil)
            except:
                math_text = ""
        else:
            math_text = "MOCK_MATH_OUTPUT"
        math_time += (time.time() - t0)
        
        # Evaluate Math AST/Structure (Just using the math portion of GT)
        # In this dataset, the math expression is isolated in `item["math"]`
        target_math = item["math"]
        
        # Check if the required math structure exists in the outputs
        # This is a naive check. A real AST parser would build the tree.
        tess_score = evaluate_string(tess_text, target_math)
        math_score = evaluate_string(math_text, target_math)
        
        # We consider it a "math hit" if the exact math string is found within the output
        target_math_clean = target_math.replace("$", "").replace(" ", "")
        
        if target_math_clean in tess_text.replace(" ", "").replace("$", ""):
            tess_correct += 1
            
        if target_math_clean in math_text.replace(" ", "").replace("$", ""):
            math_correct += 1
            
        results.append({
            "id": item["id"],
            "target": target_math_clean,
            "tesseract": tess_text,
            "pix2tex": math_text
        })
        
        if idx % 10 == 0:
            print(f"Processed {idx}/{len(subset)}")

    total = len(subset)
    print("\n--- BENCHMARK RESULTS ---")
    print(f"Total Evaluated: {total}")
    
    print("\nTesseract (General OCR):")
    print(f"Math Structure Accuracy: {tess_correct}/{total} ({(tess_correct/total)*100:.1f}%)")
    print(f"Avg Latency: {tess_time/total:.3f} s")
    
    print("\npix2tex (Math OCR):")
    print(f"Math Structure Accuracy: {math_correct}/{total} ({(math_correct/total)*100:.1f}%)")
    print(f"Avg Latency: {math_time/total:.3f} s")
    
    # Save results
    with open("../reports/ocr_eval_raw.json", "w") as f:
        json.dump(results, f, indent=4)
        
if __name__ == "__main__":
    run_benchmark()
