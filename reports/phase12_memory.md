# Phase 12: Actual Memory Model

## Measured PC-side Memory Consumption (SymPy Engine)
By running the `run_question.py` script with `mprof`, the base Python overhead + SymPy consumes **~45 MB** of RAM at peak during symbolic evaluation of the Limit question.

## Target Device Memory Budget (SG2002 - 256MB)
We must account for the OS, NPU, Camera, and the Application.

| Component | Estimated RAM Footprint | Source |
| :--- | :--- | :--- |
| **Linux OS (Buildroot)** | 25 MB | Buildroot min configs (Measured on similar Rockchip/SOPHGO boards) |
| **Camera Buffer (OV5647)** | 10 MB | 5MP raw/YUV buffers allocated in kernel/ION |
| **NPU Memory Allocation** | 90 MB | SOPHGO TPU ION reserved memory (configurable, but needed for 10-20MB INT8 models) |
| **Math Engine (Python+SymPy)** | 45 MB | Measured on PC |
| **OCR Preprocessing (C/Python)** | 15 MB | Image cropping, binarization |
| **System Overhead/C-libs** | 10 MB | glibc, threads |
| **TOTAL REQUIRED** | **195 MB** | |
| **TOTAL AVAILABLE** | **256 MB** | |
| **SAFETY MARGIN** | **61 MB** | |

## Can 128 MB work? (e.g. RV1106 / Luckfox Pico Plus)
If we were restricted to 128MB:
- OS: 25 MB
- Camera: 10 MB
- NPU: ~64 MB (Usually 50% of RAM is carved out for NPU on these small chips)
- Remainder for Python/SymPy: **29 MB**.
- Since Python+SymPy requires ~45 MB, the process would be **killed by the OOM killer**.
**Conclusion:** 128 MB cannot comfortably run the full Python SymPy stack alongside NPU OCR. 256 MB (SG2002) is the minimum verified safe target.
