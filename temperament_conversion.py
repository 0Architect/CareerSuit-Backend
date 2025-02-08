import numpy as np

def convert_temperament_to_features(mel, san, phleg, chlor):
    """
    Convert temperament scores into both OCEAN personality traits and aptitude scores.
    
    Parameters:
        mel (list): Melancholic scores
        san (list): Sanguine scores
        phleg (list): Phlegmatic scores
        chlor (list): Choleric scores
    
    Returns:
        dict: Dictionary of estimated features (OCEAN + Aptitudes)
    """
    # Take the average of temperament scores
    mel = np.mean(mel)
    san = np.mean(san)
    phleg = np.mean(phleg)
    chlor = np.mean(chlor)

    # Convert to OCEAN based on rough psychology-based mapping
    features = {
        "O_score": (san * 0.4) + (mel * 0.3) + (chlor * 0.3),   # Openness
        "C_score": (mel * 0.4) + (chlor * 0.4) + (phleg * 0.2), # Conscientiousness
        "E_score": (san * 0.5) + (chlor * 0.4) - (mel * 0.3) - (phleg * 0.3),  # Extraversion
        "A_score": (san * 0.4) + (phleg * 0.4) - (chlor * 0.3), # Agreeableness
        "N_score": (mel * 0.5) + (chlor * 0.3) - (san * 0.3) - (phleg * 0.3),  # Neuroticism

        # Aptitude Scores
        "Numerical Aptitude": (mel * 0.4) + (chlor * 0.3) + (phleg * 0.3),
        "Spatial Aptitude": (chlor * 0.4) + (phleg * 0.3) + (san * 0.3),
        "Perceptual Aptitude": (mel * 0.4) + (chlor * 0.3) + (san * 0.3),
        "Abstract Reasoning": (mel * 0.4) + (chlor * 0.4) + (phleg * 0.2),
        "Verbal Reasoning": (san * 0.5) + (phleg * 0.4) - (chlor * 0.3)
    }

    # Ensure scores are within reasonable bounds (0-10)
    for key in features:
        features[key] = max(0, min(10, features[key]))

    return features

# Example usage
# temperament_scores = {
#     "mel": [3, 5, 2],  # Example scores
#     "san": [7, 8, 6],
#     "phleg": [4, 3, 5],
#     "chlor": [6, 5, 7]
# }

# features_result = convert_temperament_to_features(**temperament_scores)
# print(features_result)