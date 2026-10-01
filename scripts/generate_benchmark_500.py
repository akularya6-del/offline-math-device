import os
import random
import json
import matplotlib.pyplot as plt

out_dir = "../data/benchmark_500"
os.makedirs(out_dir, exist_ok=True)

def create_question(idx):
    qtype = random.choice(["limit", "integral", "matrix", "algebra"])
    
    if qtype == "limit":
        point = random.choice(["0", "\\infty", "1", "\\pi/2"])
        num = random.choice(["\\sin x", "x^2 - 1", "e^x - 1", "1 - \\cos x"])
        den = random.choice(["x", "x - 1", "x^2"])
        ans = random.choice(["1", "2", "1/2", "e"])
        
        text = "Evaluate the limit:"
        math_expr = r"$\lim_{x \to " + point + r"} \frac{" + num + r"}{" + den + r"}$"
        opts = [ans, "0", "\\infty", "-" + ans]
        
    elif qtype == "integral":
        lower = random.choice(["0", "-1", "\\pi/4"])
        upper = random.choice(["1", "2", "\\pi/2"])
        expr = random.choice(["x^2", "\\sin x", "e^{2x}", "\\frac{1}{x^2+1}"])
        ans = random.choice(["1/3", "\\pi/4", "e^2 - 1", "0"])
        
        text = "Find the value of the integral:"
        math_expr = r"$\int_{" + lower + r"}^{" + upper + r"} " + expr + r" \, dx$"
        opts = [ans, ans + " + 1", "0", "\\frac{1}{" + ans + "}"]
        
    elif qtype == "matrix":
        a, b, c, d = [random.randint(-5, 5) for _ in range(4)]
        matrix = f"\\left[\\begin{{array}}{{cc}} {a} & {b} \\\\ {c} & {d} \\end{{array}}\\right]"
        ans = str(a*d - b*c)
        
        text = f"If $A = {matrix}$, find $|A|$."
        math_expr = ""
        opts = [ans, str(-int(ans)), "0", "1"]
        
    else:
        expr = random.choice(["x^2 + 2x + 1", "\\sqrt{x^2 - 4}", "\\frac{x}{x-1}"])
        point = str(random.randint(2, 5))
        ans = str(random.randint(1, 20))
        
        text = f"If $f(x) = {expr}$, then $f({point})$ is:"
        math_expr = ""
        opts = [ans, "-" + ans, "0", "2"]
        
    opts = list(set(opts))
    while len(opts) < 4:
        opts.append(str(random.randint(-10, 10)))
    opts = opts[:4]
    random.shuffle(opts)
    
    fig = plt.figure(figsize=(6, 3), dpi=150)
    y = 0.8
    fig.text(0.05, y, f"Q{idx}. {text}", fontsize=12, va='top')
    
    if math_expr:
        y -= 0.3
        fig.text(0.5, y, math_expr, fontsize=16, ha='center', va='center')
        y -= 0.2
        
    y -= 0.2
    fig.text(0.1, y, f"(A) ${opts[0]}$", fontsize=12)
    fig.text(0.5, y, f"(B) ${opts[1]}$", fontsize=12)
    y -= 0.2
    fig.text(0.1, y, f"(C) ${opts[2]}$", fontsize=12)
    fig.text(0.5, y, f"(D) ${opts[3]}$", fontsize=12)
    
    plt.axis('off')
    img_path = os.path.join(out_dir, f"q_{idx:03d}.png")
    
    try:
        plt.savefig(img_path, bbox_inches='tight', pad_inches=0.1, facecolor='white')
    except Exception as e:
        plt.close(fig)
        return None
        
    plt.close(fig)
    
    return {
        "id": idx,
        "type": qtype,
        "text": text,
        "math": math_expr,
        "options": {"A": opts[0], "B": opts[1], "C": opts[2], "D": opts[3]},
        "expected_ans": ans,
        "image": img_path
    }

if __name__ == "__main__":
    dataset = []
    print("Generating 500 questions...")
    for i in range(500):
        gt = create_question(i)
        if gt:
            dataset.append(gt)
            
    with open(os.path.join(out_dir, "ground_truth.json"), "w") as f:
        json.dump(dataset, f, indent=4)
    print(f"Successfully generated {len(dataset)} questions.")
