import os
import matplotlib.pyplot as plt

out_dir = "../data/hard_ocr_benchmark"
os.makedirs(out_dir, exist_ok=True)

# Dataset containing catastrophic failure modes
# Format: (LaTeX string to render, description, expected_structure)
hard_cases = [
    (r"$x^2$", "Superscript vs Baseline (x2)", "x^2"),
    (r"$x_2$", "Subscript vs Baseline (x2)", "x_2"),
    (r"$2x$", "Coefficient vs Baseline", "2x"),
    (r"$x^{-1}$", "Negative Superscript", "x^{-1}"),
    (r"$x - 1$", "Subtraction", "x - 1"),
    (r"$\frac{1}{2}$", "Fraction vs Digits (12)", "1/2"),
    (r"$12$", "Digits", "12"),
    (r"$\sqrt{x}$", "Radical vs V", "\\sqrt{x}"),
    (r"$Vx$", "V Variable", "Vx"),
    (r"$\int x dx$", "Integral vs f", "\\int"),
    (r"$f x dx$", "Function f", "f x dx"),
    (r"$\sum x$", "Summation vs E", "\\sum"),
    (r"$E x$", "Variable E", "E x"),
    (r"$x \leq 2$", "Less than equal", "\\leq"),
    (r"$x < 2$", "Less than", "<"),
    (r"$|x|$", "Absolute value", "|x|"),
    (r"$\sin^{-1} x$", "Inverse Trig vs Trig", "\\sin^{-1} x"),
    (r"$\sin x$", "Trig", "\\sin x"),
    (r"$\frac{dy}{dx}$", "Derivative fraction", "\\frac{dy}{dx}"),
    (r"$dy dx$", "Variables", "dy dx"),
    (r"$\frac{x+1}{x-1}$", "Complex fraction", "\\frac{x+1}{x-1}"),
    (r"$x + \frac{1}{x} - 1$", "Mixed fraction", "x + \\frac{1}{x} - 1")
]

def render_equation(expr, idx, desc):
    fig = plt.figure(figsize=(4, 1), dpi=150)
    fig.text(0.5, 0.5, expr, fontsize=20, ha='center', va='center')
    plt.axis('off')
    # Use description in filename to make it easy to identify
    clean_desc = desc.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
    clean_path = os.path.join(out_dir, f"hard_{idx:02d}_{clean_desc}.png")
    plt.savefig(clean_path, bbox_inches='tight', pad_inches=0.1, facecolor='white')
    plt.close(fig)

if __name__ == "__main__":
    for i, (expr, desc, expected) in enumerate(hard_cases):
        render_equation(expr, i, desc)
    print(f"Generated {len(hard_cases)} hard benchmark images.")
