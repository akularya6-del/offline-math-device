# Phase 13: Actual Latency Model

## Measured PC-side Latency
Executed on a Mac (M-series / x86_64) using `scripts/evaluate_solver.py` and `scripts/run_question.py`.
- **SymPy Integral Solve & Verify:** 0.092 s
- **SymPy Limit Solve & Verify:** 0.158 s
- **Tesseract OCR (Clean Math Image):** 0.069 s
- **Total PC Time:** ~0.25 - 0.35 s

## Estimated Target Hardware Latency (SG2002 - 1GHz RISC-V + 1 TOPS NPU)
The SG2002 is significantly slower than a PC for single-thread Python, but highly optimized for neural networks.

| Pipeline Stage | PC Measured | Target Estimated | Notes |
| :--- | :--- | :--- | :--- |
| **Camera Capture** | N/A | 0.300 s | Sensor init, AE/AWB settling (3 frames) |
| **Image Preprocessing** | N/A | 0.200 s | Crop, resize, normalize (C-accelerated) |
| **OCR Inference (NPU)** | 0.069 s (Tesseract) | 0.800 s | Assuming ~10-20MB INT8 model at 1 TOPS. *Requires Physical Validation.* |
| **Parser / String cleanup** | 0.005 s | 0.050 s | Python string ops |
| **Math Engine (SymPy)** | 0.158 s | 3.500 s | RISC-V 1GHz is ~20x slower than modern desktop CPU for raw Python |
| **Total Latency** | **~0.3 s** | **~4.85 s** | |

## Conclusion
The end-to-end latency is estimated at **~4.85 seconds**. This meets the 5-second target, but the SymPy evaluation time on a 1GHz RISC-V core is the biggest bottleneck.
