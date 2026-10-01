import sys
import os

# Add src to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from solver.calculus_solver import CalculusSolver
from solver.matrix_solver import MatrixSolver
from solver.algebra_solver import AlgebraSolver

class QuestionRouter:
    def __init__(self):
        self.calc_solver = CalculusSolver()
        self.matrix_solver = MatrixSolver()
        self.alg_solver = AlgebraSolver()

    def route_and_solve(self, question_dict):
        """
        Routes the question to the appropriate solver based on topic/IR.
        """
        
        ir = question_dict.get("math_ir", {})
        q_type = ir.get("type", "")
        
        if not q_type:
            # Fallback to simple keyword routing if no IR
            text = question_dict.get("question_text", "").lower()
            if "lim" in text or "integral" in text or "derivative" in text:
                return self.calc_solver.solve(question_dict)
            elif "matrix" in text or "det(" in text:
                return self.matrix_solver.solve(question_dict)
            else:
                return self.alg_solver.solve(question_dict)
                
        # Route based on IR type
        if q_type in ["limit", "integral", "derivative"]:
            return self.calc_solver.solve(question_dict)
        elif q_type in ["matrix_algebra", "determinant"]:
            return self.matrix_solver.solve(question_dict)
        else:
            return self.alg_solver.solve(question_dict)
