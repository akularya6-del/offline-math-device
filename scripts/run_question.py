import sys
import os
import json
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from solver.router import QuestionRouter

def run_pipeline(question_id, json_path="data/cuet_questions_ir.json"):
    print(f"--- STARTING PIPELINE FOR QUESTION {question_id} ---")
    start_total = time.time()
    
    # 1. Image Capture / Preprocessing (Simulated)
    print("Capturing Image...")
    time.sleep(0.1) # Simulate camera delay
    
    # 2. OCR (Simulated by loading from JSON)
    print("Running OCR...")
    time.sleep(0.5) # Simulate NPU text detection/recognition delay
    
    with open(json_path, 'r') as f:
        questions = json.load(f)
        
    q = next((item for item in questions if item["question_id"] == str(question_id)), None)
    if not q:
        print("Question not found in dataset.")
        return
        
    # Output Question Text (as requested)
    print("\nQuestion:")
    print(q["question_text"][:200] + "...")
    
    # Simulate OCR parsing failure if no Math IR
    has_ir = "math_ir" in q
    if has_ir:
        print("\nOCR (Structured):")
        print(q["math_ir"]["expr"])
    else:
        print("\nOCR (Unstructured - FAILED):")
        print("Failed to extract structural math from image.")
    
    # 3. Parsed Representation
    print("\nParsed representation:")
    if has_ir:
        print(json.dumps(q["math_ir"], indent=2))
    else:
        print("None")
        
    # 4. Math Solver & Verifier
    router = QuestionRouter()
    
    t_solve_start = time.time()
    ans, conf, reason = router.route_and_solve(q)
    t_solve = time.time() - t_solve_start
    
    print("\nTopic:")
    print(q.get("math_ir", {}).get("type", "Unknown"))
    
    print("\nPrimary solution & Independent verification:")
    print(reason)
    
    print("\nOptions:")
    for k, v in q["options"].items():
        print(f"{k}: {v.strip()}")
        
    print("\nSelected:")
    print(ans)
    
    print("\nConfidence:")
    print(conf)
    
    t_total = time.time() - start_total
    print(f"\nProcessing time:")
    print(f"{t_total:.3f} s")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_pipeline(sys.argv[1])
    else:
        print("Running for Limit Question (8):")
        run_pipeline("8")
        print("\n" + "="*50 + "\n")
        print("Running for Integral Question (4):")
        run_pipeline("4")
