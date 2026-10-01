import json

q_ir = {
    "1": {
        "type": "matrix_algebra",
        "expr": "A**3 - 6*A**2 + 11*A - 6*I = 0; B = A**2 - 5*A + 7*I; det(A)=6",
        "target": "det(B)"
    },
    "4": {
        "type": "integral",
        "expr": "(x**2 + 1)/(x**4 + 1)",
        "var": "x",
        "options_clean": {
            "A": "(1/sqrt(2)) * atan((x**2 - 1)/(sqrt(2)*x))",
            "B": "atan(x)",
            "C": "log(x**2 + 1)",
            "D": "2*x / (x+1)"
        }
    },
    "8": {
        "type": "limit",
        "expr": "(1/x**2) * log(((1+sin(x))/(1-sin(x)))**tan(x))",
        "var": "x",
        "point": "0",
        "options_clean": {
            "A": "1",
            "B": "2",
            "C": "4",
            "D": "0"
        }
    }
}

with open("/Users/racoon/Documents/OFFLINE CUET/offline_math_device/data/cuet_questions.json", "r") as f:
    qs = json.load(f)
    
for q in qs:
    if q["question_id"] in q_ir:
        q["math_ir"] = q_ir[q["question_id"]]

with open("/Users/racoon/Documents/OFFLINE CUET/offline_math_device/data/cuet_questions_ir.json", "w") as f:
    json.dump(qs, f, indent=4)
