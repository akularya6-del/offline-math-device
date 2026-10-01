import cv2
import re
import numpy as np

class TokenMathClassifier:
    MATH_VOCAB = {"lim", "sin", "cos", "tan", "log", "det", "dy", "dx", "dt", "dz", "if", "let", "then"}
    # Note: 'if', 'let', 'then' are text, so we should exclude them.
    TEXT_VOCAB = {"if", "let", "then", "the", "a", "an", "is", "are", "be", "find", "value", "of", "and", "or", "for", "all", "which", "following", "true", "false", "evaluate", "equation", "matrix"}

    @staticmethod
    def is_math_token(text):
        text_lower = text.lower()
        
        # Explicit text overrides
        if text_lower in TokenMathClassifier.TEXT_VOCAB:
            return False
            
        # Math vocab overrides
        if text_lower in {"lim", "sin", "cos", "tan", "log", "det", "cot", "sec", "csc"}:
            return True
            
        # Contains operators or brackets
        if re.search(r'[=\+\-\/\*\<\>\|\(\)\[\]\{\}\^\_\∫\√\≤\≥\∞]', text):
            return True
            
        # Contains digits
        if re.search(r'\d', text):
            # purely digits could be math or just a number in text, but we'll lean math for reconstruction
            return True
            
        # Single letters (often variables like x, y, a, b, A, B)
        if len(text) == 1 and text.isalpha() and text_lower not in {"a", "i"}:
            return True
            
        # Mix of letters and digits (e.g. x2)
        if re.search(r'[a-zA-Z]', text) and re.search(r'\d', text):
            return True
            
        return False

    @staticmethod
    def group_math_spans(tokens, x_threshold=30, y_threshold=20):
        """
        Groups adjacent math tokens into unified bounding boxes.
        tokens: list of dicts {'text': str, 'bbox': (x1,y1,x2,y2), 'is_math': bool}
        """
        math_tokens = [t for t in tokens if t['is_math']]
        if not math_tokens:
            return []

        # Simple hierarchical clustering based on bounding box distances
        groups = []
        for t in math_tokens:
            x1, y1, x2, y2 = t['bbox']
            placed = False
            for g in groups:
                gx1, gy1, gx2, gy2 = g['bbox']
                
                # Check horizontal and vertical distance
                dx = max(0, max(gx1 - x2, x1 - gx2))
                dy = max(0, max(gy1 - y2, y1 - gy2))
                
                # If close enough, merge into this group
                if dx < x_threshold and dy < y_threshold:
                    g['bbox'] = (min(gx1, x1), min(gy1, y1), max(gx2, x2), max(gy2, y2))
                    g['tokens'].append(t)
                    placed = True
                    break
            
            if not placed:
                groups.append({
                    'bbox': (x1, y1, x2, y2),
                    'tokens': [t]
                })
                
        # Merge intersecting or very close groups (iterative)
        merged_groups = []
        while groups:
            curr = groups.pop(0)
            cx1, cy1, cx2, cy2 = curr['bbox']
            
            i = 0
            while i < len(groups):
                g = groups[i]
                gx1, gy1, gx2, gy2 = g['bbox']
                dx = max(0, max(cx1 - gx2, gx1 - cx2))
                dy = max(0, max(cy1 - gy2, gy1 - cy2))
                
                if dx < x_threshold and dy < y_threshold:
                    curr['bbox'] = (min(cx1, gx1), min(cy1, gy1), max(cx2, gx2), max(cy2, gy2))
                    curr['tokens'].extend(g['tokens'])
                    groups.pop(i)
                    i = 0 # Restart checks after expansion
                else:
                    i += 1
            merged_groups.append(curr)
            
        return merged_groups

    @staticmethod
    def extract_tokens(img_cv):
        import pytesseract
        data = pytesseract.image_to_data(img_cv, output_type=pytesseract.Output.DICT)
        tokens = []
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            if text:
                left = data['left'][i]
                top = data['top'][i]
                width = data['width'][i]
                height = data['height'][i]
                is_math = TokenMathClassifier.is_math_token(text)
                tokens.append({
                    'text': text,
                    'bbox': (left, top, left+width, top+height),
                    'is_math': is_math,
                    'conf': data['conf'][i]
                })
        return tokens
