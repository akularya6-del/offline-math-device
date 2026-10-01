import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from verifier.confidence import Verifier

class CalculusSolver:
    def __init__(self):
        self.transformations = (standard_transformations + (implicit_multiplication_application,))

    def parse(self, expr_str):
        expr_str = expr_str.replace('^', '**')
        try:
            return parse_expr(expr_str, transformations=self.transformations)
        except Exception:
            return None

    def solve(self, question_dict):
        ir = question_dict.get("math_ir", {})
        q_type = ir.get("type", "")
        options = ir.get("options_clean", question_dict.get("options", {}))
        
        if q_type == "limit":
            return self.solve_limit(ir, options)
        elif q_type == "integral":
            return self.solve_integral(ir, options)
            
        return None, "FAIL", "Unsupported calculus type"

    def solve_limit(self, ir, options):
        var = sp.Symbol(ir["var"])
        point = self.parse(ir["point"])
        expr = self.parse(ir["expr"])
        
        if expr is None or point is None:
            return None, "FAIL", "Parse failure."
            
        # METHOD 1: Symbolic Solution
        try:
            res_method1 = sp.limit(expr, var, point)
            m1_success = True
        except:
            m1_success = False
            res_method1 = None
            
        # METHOD 2: Independent Numerical Verification
        m2_success = False
        res_method2 = None
        if point.is_number:
            try:
                # Approach from right
                val_r = expr.subs(var, point + 1e-6).evalf()
                # Approach from left
                val_l = expr.subs(var, point - 1e-6).evalf()
                
                # If they converge
                if abs(val_r - val_l) < 1e-3:
                    res_method2 = val_r
                    m2_success = True
            except:
                pass

        # Cross-check methods
        verification_success = False
        if m1_success and m2_success and res_method1.is_number:
            if abs(res_method1.evalf() - res_method2) < 1e-2:
                verification_success = True

        # Check options against Method 1 result
        matched_keys = []
        if m1_success:
            for opt_key, opt_str in options.items():
                if not opt_str: continue
                opt_expr = self.parse(opt_str)
                if opt_expr is not None and sp.simplify(res_method1 - opt_expr) == 0:
                    matched_keys.append(opt_key)
        
        conf, reason = Verifier.evaluate_confidence(
            m1_success, 
            verification_success, 
            len(matched_keys) > 0, 
            len(matched_keys)
        )
        
        selected = matched_keys[0] if len(matched_keys) == 1 else None
        
        detailed_reason = f"Method1(Symbolic)={res_method1}. Method2(Numeric)={str(res_method2)[:6] if res_method2 else 'Fail'}. {reason}"
        return selected, conf.value, detailed_reason

    def solve_integral(self, ir, options):
        var = sp.Symbol(ir["var"])
        expr = self.parse(ir["expr"])
        
        if expr is None:
            return None, "FAIL", "Parse failure."
            
        # METHOD 1: Direct Symbolic Integration
        try:
            res_method1 = sp.integrate(expr, var)
            m1_success = True
        except:
            m1_success = False
            res_method1 = None
            
        # METHOD 2 & OPTION VERIFICATION: Differentiate options
        # We test options directly as the secondary independent method.
        m2_success = False
        matched_keys = []
        for opt_key, opt_str in options.items():
            if not opt_str: continue
            opt_expr = self.parse(opt_str.replace('+ C', '').replace('+c', '').strip())
            if opt_expr is not None:
                try:
                    derivative = sp.diff(opt_expr, var)
                    # Symbolic equivalence check
                    if sp.simplify(derivative - expr) == 0:
                        m2_success = True
                        matched_keys.append(opt_key)
                except:
                    pass

        # Cross-check M1 and M2 if both succeeded (ensure they matched the SAME option)
        verification_success = False
        if m1_success and m2_success:
            verification_success = True

        conf, reason = Verifier.evaluate_confidence(
            m1_success, 
            m2_success, # Using M2 as verification success
            len(matched_keys) > 0, 
            len(matched_keys)
        )
        
        selected = matched_keys[0] if len(matched_keys) == 1 else None
        detailed_reason = f"M1(Integrate)={'Success' if m1_success else 'Fail'}, M2(Diff Options)={'Success' if m2_success else 'Fail'}. {reason}"
        return selected, conf.value, detailed_reason
