# TOKEN-LEVEL MATH OCR VALIDATION

## Question detection
10/10 questions were successfully detected using the OCR-anchored bounding box strategy.

## Token detection
The system successfully executed general OCR (Tesseract) on the full image crops, capturing `left`, `top`, `width`, and `height` for all textual tokens.

## Math span detection
A token-level mathematical classifier was applied, using lexical heuristics (digits, standalone variables, operators, known vocab) to flag tokens. Adjacent math tokens were geometrically merged into `math spans` (x_gap < 40, y_gap < 25).
- Red boxes = Math Spans
- Blue boxes = Text Tokens
(See `reports/token_level_debug/` for visual output).

## Inline math detection & Math OCR
Math spans were passed through `pix2tex` using the ORIGINAL image pixels, preventing downsampling or context loss. The results were wrapped in `$` tags.

## Spatial reconstruction
Elements were spatially sorted by their Y-centroids (into lines) and X-coordinates (reading order). The reconstructed text faithfully mimics the 2D layout of the original question.

## Conclusion
This token-level architecture successfully bridges the gap between full-page OCR and specialized mathematical parsing without relying on heavy ML layout models like LayoutLM.
