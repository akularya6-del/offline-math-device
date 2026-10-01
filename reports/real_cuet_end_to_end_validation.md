# REAL CUET END-TO-END VALIDATION

## Dataset
32 questions / 5 pages

## Whole-question reconstruction
0/32 (The layout segmentation heuristics failed to cleanly separate the complex nested fractions/matrices from the text blocks on the real images. It frequently cut equations in half.)

## Math AST
0/32 (Because the bounding boxes were imprecise, `pix2tex` received truncated math strings, leading to hallucinations.)

## Option extraction
0/32 (Options were clumped horizontally and misread by Tesseract).

## Solver agreement
0/32 (Syntax Error. The raw LaTeX output from pix2tex cannot be directly consumed by SymPy without a topological mapper layer).

## Final Results
Final correct: 0/32
Incorrect (False Answer): 0/32
Abstained: 32/32
False-answer rate: 0.0%

## Timing
Mean latency: 0.89 sec
P95 latency: 2.06 sec
Maximum latency: 4.66 sec
Total processing time: 0.48 min

## Failure taxonomy
- **Segmentation Failure:** OpenCV bounding box heuristics (dilation) completely fail on multi-line equations, matrices, and tightly packed options.
- **Math Parser Failure:** Passing raw LaTeX to SymPy fails immediately.
- **Verification Trigger:** The system correctly identified the layout mismatch and abstained safely on 100% of the questions.

## Architecture Decision
A. **Most accurate host architecture:** LayoutLM / Surya-OCR for layout detection + a robust LaTeX-to-SymPy IR mapper.
B. **Remaining errors:** OpenCV heuristics cannot parse CUET test pages.
C. **Hardware Implications:** The minimum required architecture (Layout Transformer + ViT Math OCR) inherently requires >512MB RAM.
