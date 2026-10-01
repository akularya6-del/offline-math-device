# CRITICAL NEW OBJECTIVE: PERFECT QUESTION RECONSTRUCTION

## 1. The Catastrophic Failure of Standard OCR
As physically proven by the `test_hard_ocr.py` benchmark, standard text recognition (Tesseract v5) completely destroys mathematical notation:
- `x^2` became `x2`
- `\frac{x+1}{x-1}` became `eat`
- `\int x dx` became `J xdx`

If the mathematical solver receives `eat` or `x2`, it will output a wrong answer (or fail). Therefore, a mathematically correct solution does NOT prove the OCR was correct. **Perfect question reconstruction is the single most critical dependency of this project.**

## 2. The New Hybrid OCR Architecture
The new architecture abandons linear text OCR in favor of a structurally aware, multi-pass hypothesis system:

```text
IMAGE 
  ↓ 
Document/Math Region Detector (YOLO/RT-DETR)
  ↓ 
Math Symbol Recognizer + Spatial Parser (e.g. UniMERNet / pix2tex)
  ↓ 
CANDIDATE HYPOTHESIS GENERATION (Pass A, B, C...)
  ↓ 
IMAGE-TO-TEXT SPATIAL BACKCHECK (e.g. Is the '2' physically above the 'x' baseline?)
  ↓ 
QUESTION CONSISTENCY CHECK (Does the math make sense over the Reals?)
  ↓ 
MATH INTERMEDIATE REPRESENTATION (AST)
  ↓ 
(Hand-off to Deterministic Solver)
```

## 3. The "Recapture" Protocol
If the spatial backcheck cannot resolve an ambiguity (e.g., the '2' is exactly on the boundary between a subscript and a coefficient), the system must **ABSTAIN and command a RECAPTURE**. It is better to fail than to provide a mathematically correct answer to a misread question.

## 4. Hardware Implications: Optical Design for OCR
We must design the camera system specifically as a mathematical document scanner, not a generic camera:
- **Focal Distance:** Must be mechanically fixed (e.g. a transparent acrylic standoff at exactly 60mm) to guarantee perfect focus on the OV5647.
- **Illumination:** A diffused white LED ring is required to eliminate shadows which corrupt fraction bars and minus signs.
- **Resolution:** The camera must provide enough pixels-per-character (PPC) to resolve the gap between a minus sign and a fraction bar.

## 5. Next Immediate Engineering Steps
Before returning to custom PCB design or hardware sizing, we must:
1. Benchmark `UniMERNet` and `pix2tex` on the `hard_ocr_benchmark` dataset.
2. Build the AST parser to convert LaTeX output from these models into the SymPy AST.
3. Test if `pix2tex` can be quantized to INT8 and run on the SG2002's 1 TOPS NPU within the 195MB memory budget. If it cannot, we must search for a heavier SoC (e.g., RV1126 or a Rockchip RK3566).
