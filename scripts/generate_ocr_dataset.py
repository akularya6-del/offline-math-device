import os
import random
import matplotlib.pyplot as plt
import cv2
import numpy as np

out_clean = "../data/ocr_test_clean"
out_deg = "../data/ocr_test_degraded"
os.makedirs(out_clean, exist_ok=True)
os.makedirs(out_deg, exist_ok=True)

expressions = [
    r"$x^2 + y^2 = r^2$",
    r"$\int_0^1 x^2 dx$",
    r"$\lim_{x \to 0} \frac{\sin x}{x} = 1$",
    r"$\frac{dy}{dx} = 2x + 3$",
    r"$\sum_{i=1}^n i = \frac{n(n+1)}{2}$",
    r"$\sqrt{x^2 + 1}$",
    r"$e^{i\pi} + 1 = 0$",
    r"$f(x) = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$",
    r"$\vec{v} = 2\hat{i} + 3\hat{j} - \hat{k}$"
]

def render_equation(expr, idx):
    fig = plt.figure(figsize=(4, 1), dpi=150)
    fig.text(0.5, 0.5, expr, fontsize=20, ha='center', va='center')
    plt.axis('off')
    clean_path = os.path.join(out_clean, f"eq_{idx:03d}.png")
    plt.savefig(clean_path, bbox_inches='tight', pad_inches=0.1, facecolor='white')
    plt.close(fig)
    return clean_path

def degrade_image(img_path, idx):
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    
    if random.random() > 0.3:
        img = cv2.GaussianBlur(img, (5, 5), 0)
        
    if random.random() > 0.3:
        noise = np.random.normal(0, 15, img.shape).astype(np.uint8)
        img = cv2.add(img, noise)
        
    if random.random() > 0.5:
        gradient = np.zeros_like(img, dtype=np.float32)
        for y in range(h):
            gradient[y, :] = 1.0 - (y / h) * 0.4
        img = (img * gradient).astype(np.uint8)
        
    if random.random() > 0.3:
        angle = random.uniform(-3, 3)
        M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
        img = cv2.warpAffine(img, M, (w, h), borderValue=(255,255,255))
        
    deg_path = os.path.join(out_deg, f"eq_deg_{idx:03d}.png")
    cv2.imwrite(deg_path, img)

if __name__ == "__main__":
    for i in range(100):
        expr = expressions[i % len(expressions)]
        clean_path = render_equation(expr, i)
        degrade_image(clean_path, i)
    print(f"Generated 100 clean and 100 degraded images.")
