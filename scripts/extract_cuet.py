import re
import json

def parse_questions(filepath):
    with open(filepath, 'r') as f:
        text = f.read()

    # Split by questions (e.g. "1. Let A...")
    parts = re.split(r'\n(?=\d+\.\s)', text)
    
    # The first part is the header. The rest are questions.
    header = parts[0]
    raw_questions = parts[1:]
    
    questions = []
    
    for raw in raw_questions:
        raw = raw.strip()
        
        # Extract question number
        match = re.match(r'(\d+)\.\s+(.*)', raw, re.DOTALL)
        if not match:
            continue
            
        q_id = match.group(1)
        rest = match.group(2)
        
        # Split options from question text
        # Options usually start with (A), (B), (C), (D)
        
        options_dict = {"A": "", "B": "", "C": "", "D": ""}
        q_text = rest
        
        opt_matches = list(re.finditer(r'\n\s*\(([A-D])\)\s+(.*?)(?=\n\s*\([A-D]\)|\Z)', rest, re.DOTALL))
        
        if opt_matches:
            # The question text is everything before the first option
            first_opt_start = opt_matches[0].start()
            q_text = rest[:first_opt_start].strip()
            
            for m in opt_matches:
                opt_letter = m.group(1)
                opt_text = m.group(2).strip()
                options_dict[opt_letter] = opt_text
                
        questions.append({
            "question_id": q_id,
            "question_text": q_text,
            "options": options_dict,
            "topic": "",
            "subtopic": "",
            "requires_diagram": False,
            "ocr_difficulty": "",
            "parser_difficulty": "",
            "solver_difficulty": "",
            "classification": "",
            "expected_answer": "",
            "source_page": ""
        })
        
    return questions

if __name__ == "__main__":
    filepath = "/tmp/cuet_questions.txt"
    outpath = "/Users/racoon/Documents/OFFLINE CUET/offline_math_device/data/cuet_questions.json"
    qs = parse_questions(filepath)
    
    with open(outpath, 'w') as f:
        json.dump(qs, f, indent=4)
        
    print(f"Extracted {len(qs)} questions to {outpath}")
