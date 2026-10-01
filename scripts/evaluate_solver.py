import json
import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from solver.router import QuestionRouter

def run_evaluation(json_path):
    with open(json_path, 'r') as f:
        questions = json.load(f)
        
    router = QuestionRouter()
    results = []
    
    print(f"{'Q#':<5} | {'Result':<6} | {'Conf':<10} | {'Time(s)':<7} | Reasoning")
    print("-" * 80)
    
    for q in questions:
        q_id = q['question_id']
        start = time.time()
        ans, conf, reason = router.route_and_solve(q)
        t = time.time() - start
        
        print(f"{q_id:<5} | {str(ans):<6} | {conf:<10} | {t:<7.3f} | {reason[:60]}...")
        
        q['solver_result'] = ans
        q['solver_confidence'] = conf
        q['solver_reasoning'] = reason
        q['processing_time_pc_measured'] = t
        results.append(q)
        
    return results

if __name__ == "__main__":
    json_path = "/Users/racoon/Documents/OFFLINE CUET/offline_math_device/data/cuet_questions_ir.json"
    results = run_evaluation(json_path)
    
    out_path = "/Users/racoon/Documents/OFFLINE CUET/offline_math_device/reports/cuet_solver_results.json"
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=4)
