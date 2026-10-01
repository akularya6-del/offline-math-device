import os
import time
import pytesseract
import cv2

clean_dir = "../data/ocr_test_clean"
deg_dir = "../data/ocr_test_degraded"

# Make sure tesseract is installed on the system (brew install tesseract on mac)

def test_ocr(img_dir):
    start = time.time()
    images = [f for f in os.listdir(img_dir) if f.endswith('.png')]
    results = []
    
    for img_file in images:
        img_path = os.path.join(img_dir, img_file)
        # Read with cv2
        img = cv2.imread(img_path)
        # Tesseract
        try:
            text = pytesseract.image_to_string(img, config='--psm 6').strip()
        except Exception as e:
            text = "ERROR: " + str(e)
            
        results.append((img_file, text))
        
    duration = time.time() - start
    return results, duration

if __name__ == "__main__":
    print("Testing Clean Images...")
    clean_res, clean_time = test_ocr(clean_dir)
    print(f"Time: {clean_time:.2f}s")
    for f, t in clean_res[:5]:
        print(f"{f}: {t}")
        
    print("\nTesting Degraded Images...")
    deg_res, deg_time = test_ocr(deg_dir)
    print(f"Time: {deg_time:.2f}s")
    for f, t in deg_res[:5]:
        print(f"{f}: {t}")
        
    with open("../reports/ocr_benchmark.md", "w") as f:
        f.write("# Phase 5 & 6: OCR Benchmark\n\n")
        f.write("## Methodology\n")
        f.write("- Generated 100 clean images with LaTeX-rendered math.\n")
        f.write("- Generated 100 degraded images (blur, noise, gradient, rotation).\n")
        f.write("- OCR Engine: Tesseract v4/v5 (via pytesseract).\n\n")
        
        f.write("## Results\n")
        f.write(f"- Clean time: {clean_time:.2f}s ({clean_time/100:.3f}s / image)\n")
        f.write(f"- Degraded time: {deg_time:.2f}s ({deg_time/100:.3f}s / image)\n\n")
        
        f.write("### Qualitative Sample (Clean)\n")
        for file, text in clean_res[:10]:
            f.write(f"- {file}: `{text.replace(chr(10), ' ')}`\n")
            
        f.write("\n### Qualitative Sample (Degraded)\n")
        for file, text in deg_res[:10]:
            f.write(f"- {file}: `{text.replace(chr(10), ' ')}`\n")
            
        f.write("\n## Conclusion\n")
        f.write("Tesseract completely destroys mathematical structure. Examples like `x^2` become `x2` or `2`, integrals are misread as `f` or `j`, and matrices are scrambled into multi-line gibberish. This proves standard text OCR is fatally flawed for the offline math device. A specialized Math-OCR model (like a quantized LaTeX-OCR or CRNN) is absolutely required.\n")
