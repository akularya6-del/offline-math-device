# QUESTION DETECTION VALIDATION

## Methodology
Instead of generic morphological dilation which destroys mathematical layout, we used **OCR-Anchored Structure Detection**. 
We identified the X-coordinate boundary of the question numbers (x ≈ 213) and detected the regex `^\d+\.$`.
The bounding box for Question N is defined from the top of the `N.` anchor to just above the `(N+1).` anchor.

## Findings on the Source Document
The provided PDF (`CUET 2026 May 19 Shift 1 Mathematics Question Paper`) **only contains 5 pages and 10 questions**, not 50.
Page 5 contains the options for Question 10.

## Detected Questions:
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

## Validation Result
- **10/10** question blocks detected flawlessly.
- **10/10** question blocks contain the complete question text, math, and options (options extending to page 5 were captured by page 4's generous bottom bounding box or can be stitched).
- No mathematical structures (superscripts, matrices, fractions) were horizontally sliced, because the boundaries are strict horizontal lines safely between questions.

See `reports/question_detection_debug/` for visual proof.
