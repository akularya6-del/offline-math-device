from enum import Enum

class ConfidenceLevel(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    FAIL = "FAIL"

class Verifier:
    @staticmethod
    def evaluate_confidence(primary_success, verification_success, options_matched, num_options_matched, constraints_met=True):
        """
        Evaluates the confidence level of a solved answer.
        
        Args:
            primary_success (bool): Did the primary solver produce a result?
            verification_success (bool): Did the independent verification pass?
            options_matched (bool): Did the result match at least one option?
            num_options_matched (int): How many options matched the result? (Should be exactly 1)
            constraints_met (bool): Are mathematical constraints met? (e.g., probability between 0 and 1)
        """
        if not constraints_met:
            return ConfidenceLevel.FAIL, "Mathematical constraints violated."
            
        if not primary_success and not verification_success:
            return ConfidenceLevel.FAIL, "Both primary solve and verification failed."
            
        if num_options_matched > 1:
            return ConfidenceLevel.LOW, f"Ambiguous match: result matched {num_options_matched} options."
            
        if not options_matched:
            if primary_success and verification_success:
                return ConfidenceLevel.LOW, "Solved and verified, but matched no options."
            return ConfidenceLevel.FAIL, "Did not match any options."

        # If exactly one option matched
        if primary_success and verification_success:
            return ConfidenceLevel.HIGH, "Primary solve and independent verification succeeded. Exact 1 option match."
            
        if primary_success or verification_success:
             return ConfidenceLevel.MEDIUM, "Only one of primary solve or verification succeeded, but it matched exactly 1 option."
             
        return ConfidenceLevel.FAIL, "Unknown error."
