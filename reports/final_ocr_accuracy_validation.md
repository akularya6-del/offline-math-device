# Final OCR Accuracy Validation & Architecture Blueprint

## 1. The Core Paradigm Shift: Accuracy > Speed
The product target has been completely redefined. We are abandoning the theoretical 5-second per question constraint. The new constraint is **maximum verified mathematical accuracy** within a budget of **60 minutes for 50 questions (Average: 72 seconds/question)**. 

If a question requires 60 seconds of multi-pass optical processing to confidently distinguish $x^2$ from $x_2$, the system will consume that budget. A wrong answer derived from bad OCR is a fatal system failure. The system prioritizes `ABSTAIN/NO ANSWER` over `WRONG ANSWER`.

## 2. Benchmark Datasets
- **Real CUET Ground Truth:** The official "CUET 2026 May 19 Shift 1 Mathematics Question Paper" PDF has been mapped for direct image-to-AST verification (covering matrices, variable powers, rational integrals, vectors, and 3D geometry).
- **Synthetic 500 Dataset:** 370 successfully generated complex CUET-style MCQs.
- **Hard OCR Dataset:** 22 catastrophic spatial-layout edge cases designed to force failures.

## 3. The Rejection of Pure Generic / Pure Math OCR
Testing proved that:
- **Architecture A (Tesseract only):** Destroyed 2D math structures (e.g. `\frac{1}{2} \rightarrow 12`).
- **Architecture B (pix2tex only):** Hallucinated English text into bizarre LaTeX variables.
- **Architecture C/D (Hybrid Spatial Architecture):** This is the **only viable path**. The image must be run through a layout detector (e.g., OpenCV contours or YOLO). Text regions go to Tesseract; Math regions go to a Mathematical OCR model; their spatial coordinates are then used to reconstruct the final question AST.

## 4. Adaptive Computation & Multi-Pass OCR
The pipeline (`src/ocr/adaptive_reconstructor.py`) executes:
1. **Image Quality Gate:** Rejects blur/glare before wasting processing time.
2. **Fast Pass:** Standard threshold + Hybrid OCR.
3. **Escalation (If Confidence < HIGH):** Exploit the 72-second budget. Run Upscaled, Grayscale, Adaptive Threshold, and Sharpened variants. 
4. **Spatial Evidence Check:** Do NOT use majority voting. Use layout evidence (e.g. centroid height) to eliminate false hypotheses.

## 5. Strict Separation of Solver and OCR
**Rule:** The mathematical solver is strictly forbidden from "fixing" OCR errors to match an answer option. 
Options A, B, C, D are used **exclusively as a final verification layer**. If the verified Math IR is solved via two independent methods (e.g. Symbolic Integration AND Differentiating the options) and yields exactly one match, the answer is output. If 0 or 2+ options match, the system investigates or abstains.

## 6. Hardware Implications
The LicheeRV Nano-B (SG2002) with 256MB RAM is now **strictly provisional**.
We will first determine the absolute most accurate Hybrid OCR architecture on the host PC. 
- If that architecture can be quantized and compiled to a `.cvimodel` that fits within the NPU's 90MB ION memory carveout, we will proceed with the SG2002.
- **If compression destroys the required question reconstruction accuracy, we will abandon the SG2002.** Hardware must support the software requirements, not the other way around. A 512MB or 1GB SoC (e.g. RK3566) will be selected if necessary.

## 7. Remaining Physical Tests
1. Generate the full baseline metric tables (Question Recon %, Math AST %, False Answer %, Abstention %, RAM, Latency) across the CUET paper using the Hybrid Spatial architecture.
2. Characterize the optical requirements (diffused LED, fixed focal distance) to physically eliminate glare and shadows, reducing the software OCR burden.
