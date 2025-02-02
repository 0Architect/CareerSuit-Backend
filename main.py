from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# Updated model for the new structure
class PersonalityInput(BaseModel):
    melancholy: list
    sanguine: list
    choleric: list
    phlegmatic: list

def calculate_temperament(responses):
    """Calculates temperament scores based on user responses."""
    temperaments = {"melancholy": 0, "sanguine": 0, "choleric": 0, "phlegmatic": 0}
    for temperament, response_list in responses.items():
        temperaments[temperament] += sum(response for response in response_list if response >= 4)
    return temperaments

def determine_dominant_temperaments(temperaments):
    """Determines the dominant and secondary temperaments."""
    sorted_temperaments = sorted(temperaments.items(), key=lambda item: item[1], reverse=True)
    dominant, secondary = sorted_temperaments[0][0], sorted_temperaments[1][0]
    dominant_score, secondary_score = sorted_temperaments[0][1], sorted_temperaments[1][1]

    if (dominant_score == secondary_score and secondary in ["Sanguine", "Choleric"]):
        dominant, secondary = secondary, dominant

    total_score = dominant_score + secondary_score
    dominant_percentage = (dominant_score * 100) / total_score if total_score else 0
    secondary_percentage = (secondary_score * 100) / total_score if total_score else 0

    if dominant_percentage == 100:
        dominant_percentage = 50
        secondary_percentage = 50

    return dominant, secondary, dominant_percentage, secondary_percentage

def recommend_fields(dominant, secondary, dominant_percentage, secondary_percentage):
    """Recommends fields of study based on temperament blend."""
    recommendations = {
        "melancholy": ["Science"],
        "sanguine": ["Art"],
        "choleric": ["Social Science"],
        "phlegmatic": ["Science", "Social Science"],
    }

    if dominant_percentage >= 90:
        return recommendations[dominant]
    elif dominant_percentage >= 70:
        return recommendations[dominant] + recommendations.get(secondary, [])
    elif dominant_percentage >= 60:
        return f"Primary: {recommendations[dominant]}, You have significant capacity in: {recommendations.get(secondary,[])}"
    elif dominant_percentage >= 50:
        return f"Consider core courses in: {recommendations[dominant]} or {recommendations.get(secondary,[])}"
    else:
        return f"You have capacity for core study areas of both: {recommendations[dominant]} and {recommendations.get(secondary,[])}"

@app.post("/predict")
def predict(input_data: PersonalityInput):
    responses = input_data.dict()

    # Step 1: Calculate Temperament Scores
    temperaments = calculate_temperament(responses)

    # Step 2: Determine Dominant and Secondary Temperaments
    dominant, secondary, dominant_percentage, secondary_percentage = determine_dominant_temperaments(temperaments)

    # Step 3: Recommend Fields of Study
    recommended_fields = recommend_fields(dominant, secondary, dominant_percentage, secondary_percentage)

    # Step 4: Generate API Response
    return {
        "temperaments": [
            {"name": dominant, "percentage": dominant_percentage, "description": f"The user's responses indicate strong alignment with {dominant} traits."},
            {"name": secondary, "percentage": secondary_percentage, "description": f"The user's responses indicate moderate alignment with {secondary} traits."}
        ],
        "recommendations": {
            "primary": {
                "fieldOfStudy": {"name": recommended_fields[0], "description": "Best fit based on temperament."},
                "courseOfStudy": [{"name": "Sample Course 1", "description": "Course description here."}]
            },
            "secondary": {
                "fieldOfStudy": {"name": recommended_fields[1] if len(recommended_fields) > 1 else "None", "description": "Alternate field based on temperament."},
                "courseOfStudy": [{"name": "Sample Course 2", "description": "Course description here."}]
            }
        },
        "successStories": [
            {"imageUrl": "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQ4oVi8944egiCelyCWnDcUBUT7mAxldEx0bqKR-cWCxO32kjUbQlHw7ZNPzzL2F_MUT7leTQGpsjwYVjU0Tl8rACaKqW25g64v6TvGfw", "name": "Elon Musk", "description": "Success story of a person with this temperament."}
        ],
        "youAndYourCareer": "AI-generated text about how your personality fits into the career world."
    }