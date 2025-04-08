import random

def analyze_document(content, doc_type):
    """
    Analyze a document for Responsible AI metrics
    
    In a real implementation, this would use actual NLP/AI models for:
    - Bias detection
    - Hallucination detection
    - Security/privacy risk assessment
    
    For this MVP, we'll use a simplified implementation
    """
    # Simulate RAI analysis with reasonable defaults
    # In a real implementation, this would use actual models
    
    # Calculate a bias score (0-1, lower is better)
    # This would normally use a trained model to detect bias in language
    bias_score = random.uniform(0.1, 0.4)
    
    # Determine bias level based on the score
    if bias_score < 0.2:
        bias_level = "low"
    elif bias_score < 0.5:
        bias_level = "medium"
    else:
        bias_level = "high"
    
    # Hallucination detection
    # In a real system, this would check for factual assertions that can't be verified
    # For this demo, we'll randomly set it based on document type
    hallucination_risk = "low"
    if doc_type in ["proposal", "scope_of_work"] and random.random() < 0.3:
        hallucination_risk = "medium"
    
    # Security and privacy risk
    # This would assess the document for PII, sensitive data, etc.
    security_risk = "low"
    if doc_type == "nda":
        security_risk = "medium"  # NDAs often contain sensitive info
    
    # Calculate overall RAI score (0-1, higher is better)
    # This is an oversimplified calculation for demo purposes
    rai_score = 1.0 - (bias_score * 0.5 + 
                      (0.3 if hallucination_risk == "medium" else 0.1) * 0.25 +
                      (0.3 if security_risk == "medium" else 0.1) * 0.25)
    
    # Round to 2 decimal places
    rai_score = round(rai_score, 2)
    
    return {
        "score": rai_score,
        "flags": {
            "bias": {
                "level": bias_level,
                "score": round(bias_score, 2)
            },
            "hallucination": hallucination_risk,
            "security": security_risk
        }
    }

def get_rai_badge_color(score):
    """Get the color for an RAI badge based on the score"""
    if score >= 0.8:
        return "green"
    elif score >= 0.6:
        return "yellow"
    else:
        return "red"

def get_rai_explanation(flags):
    """Generate an explanation of RAI flags for the user"""
    explanations = []
    
    # Bias explanation
    bias_level = flags.get("bias", {}).get("level", "low")
    if bias_level == "high":
        explanations.append("High bias detected. The document may contain language that shows strong preferences or prejudices.")
    elif bias_level == "medium":
        explanations.append("Medium bias detected. Some language in the document may show subtle preferences.")
    else:
        explanations.append("Low bias detected. The document appears to use neutral language.")
    
    # Hallucination explanation
    hallucination = flags.get("hallucination", "low")
    if hallucination == "high":
        explanations.append("High risk of hallucination. The document may contain unverifiable claims or assertions.")
    elif hallucination == "medium":
        explanations.append("Medium risk of hallucination. Some claims in the document may benefit from verification.")
    else:
        explanations.append("Low risk of hallucination. The document appears to contain verifiable information.")
    
    # Security explanation
    security = flags.get("security", "low")
    if security == "high":
        explanations.append("High security risk. The document may contain sensitive information that requires protection.")
    elif security == "medium":
        explanations.append("Medium security risk. The document contains some information that should be handled with care.")
    else:
        explanations.append("Low security risk. The document appears to contain minimal sensitive information.")
    
    return explanations
