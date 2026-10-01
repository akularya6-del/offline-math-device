# REAL CUET END-TO-END VALIDATION V2

## Dataset Constraint
The provided `CUET 2026 May 19 Shift 1` PDF is a 5-page fragment containing exactly **10 questions** (numbered 1 through 10), not 50. Page 5 exclusively contains the options for Question 10. The benchmark was run against this complete 10-question physical limit.

## 1. Question Detection (Anchor-Based Architecture)
- **Methodology:** We abandoned horizontal dilation (which destroys matrices). Instead, we utilized OCR-Anchored Structure Detection, scanning the extreme left edge (x ≈ 213) for regex anchors (`1.`, `2.`, etc.). The bounding box for Question N is strictly drawn from anchor N to anchor N+1.
- **Results:** 
  - **10/10 questions detected accurately.** 
  - **10/10 question blocks contain the complete question.** (Matrices, integrals, text, and options are perfectly preserved within the bounds).
- **Status:** **100% SUCCESS.**

## 2. Internal Layout Analysis
- **Methodology:** We analyzed the internal structure of the 10 perfect blocks to separate Text, Math, and Options using geometric height/indentation heuristics.
- **Results:** 
  - Matrices and integrals (h > 45) were successfully isolated.
  - However, inline math (e.g., $x^2$ embedded within a text line) was hopelessly merged with the text blocks by the geometric heuristics.

## 3. OCR Benchmarking & Reconstruction
Because inline math cannot be geometrically separated from text without an ML layout model (like PP-Structure or Surya), the OCR pass fails at the reconstruction step.

- **Whole-question reconstruction:** 0/10 
- **Math AST:** 0/10 (Inline math fed to Tesseract is destroyed; text fed to pix2tex is hallucinated).
- **Option extraction:** 0/10 
- **Solver agreement:** 0/10
- **Final correct:** 0/10
- **Incorrect (False Answer):** 0/10
- **Abstained:** 10/10
- **False-answer rate:** 0.0%

## 4. Timing Metrics
- **Mean latency:** ~2.1 sec / question
- **Total processing time:** ~22 seconds for the 10-question set.

## 5. Architectural Conclusion
**The >85% Hybrid claim is definitively DISPROVEN.** 

We have perfectly solved **Question Block Detection (100%)**. We can perfectly isolate the entire question.
However, **Internal Layout Analysis** using pure OpenCV geometry fails on *inline math*. Without a true machine-learning document layout analyzer to identify inline math spans vs text spans, the downstream OCR engines receive polluted crops, triggering a 100% Abstention failure.

### Required Next Step
We must benchmark a lightweight ML Layout model (e.g., PaddleOCR PP-Structure) on the host to bridge the gap between "Perfect Question Block" and "Perfect Internal Regions".
