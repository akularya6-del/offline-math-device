# Phase 5 & 6: OCR Benchmark

## Methodology
- Generated 100 clean images with LaTeX-rendered math.
- Generated 100 degraded images (blur, noise, gradient, rotation).
- OCR Engine: Tesseract v5 (via pytesseract).

## Results
- Clean time: 6.94s (0.069s / image)
- Degraded time: 7.13s (0.071s / image)

### Qualitative Sample (Clean)
- eq_046.png (Integral): `foxtax`
- eq_052.png (Quadratic): `f(x) = abt vb" —4ac`
- eq_085.png (Summation): `n\n\n> j= ety\n2\n\ni=1`
- eq_090.png (Circle): `xe+yrar`

### Qualitative Sample (Degraded)
- eq_deg_033.png (Euler): `e™+1=0`

## Conclusion
Tesseract completely destroys mathematical structure. Examples like `x^2` become `x2` or `2`, integrals are misread as `foxtax`, and summations are scrambled into multi-line gibberish. This proves standard text OCR is fatally flawed for the offline math device. A specialized Math-OCR model (like a quantized LaTeX-OCR or CRNN) is absolutely required.
