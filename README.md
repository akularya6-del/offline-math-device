<div align="center">

# offline-math-device

**Firmware, mathematical solvers, OCR pipelines, and hardware power models for an autonomous offline mathematical calculator device.**

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![Embedded](https://img.shields.io/badge/Target-Embedded_/_Edge-blue?style=flat-square)
![OCR](https://img.shields.io/badge/OCR-Token--Level_Math-orange?style=flat-square)
![SymPy](https://img.shields.io/badge/Solver-SymPy_Engine-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

</div>

---

## 📌 Overview

**offline-math-device** contains the software architecture, token-level OCR parser, symbolic solving engine, and hardware resource models designed for a standalone physical device that captures, parses, and computes mathematical problems completely offline without internet or cloud APIs.

---

## ✨ System Architecture

```
Camera Sensor / Image Buffer
          │
          ▼
[Preprocessing & Layout Analysis] ──► Deskew, perspective crop, and line isolation
          │
          ▼
[Token-Level Math OCR] ──► Multi-pass symbol and token recognition
          │
          ▼
[AST Parser] ──► Converts tokens into Canonical Question Intermediate Representation (IR)
          │
          ▼
[Deterministic Symbolic Solver] ──► Algebra, calculus, vectors, trigonometry, and matrices
          │
          ▼
[Verifier & Formatter] ──► Validates constraints and renders step-by-step solution to display
```

---

## 🛠️ Repository Layout

- `src/preprocessing/`: Image binarization, skew rectification, and bounding box detection.
- `src/ocr/`: Token-level mathematical character recognition engine.
- `src/parser/`: Grammar definitions and AST tree generation.
- `src/solver/`: Modular symbolic solvers (algebra, calculus, probability, linear algebra).
- `src/verifier/`: Sanity checks and constraint verification.
- `scripts/`: Power consumption simulation (`power_model.py`), latency benchmarks, and hardware physical modeling (`physical_model.py`).
- `reports/`: Accuracy analysis, benchmark reports, and latency studies.

---

## 🚀 Running Benchmarks

### Prerequisites

```bash
pip install sympy opencv-python pydantic numpy
```

### Run Solver Suite

```bash
# Run token-level mathematical OCR benchmark
python3 scripts/run_token_level_benchmark.py

# Run end-to-end question detection and evaluation
python3 scripts/evaluate_solver.py
```

### Run Power & Physical Model Simulations

```bash
# Simulate power draw across operating cycles
python3 scripts/power_model.py

# Simulate hardware thermal and memory limits
python3 scripts/physical_model.py
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
