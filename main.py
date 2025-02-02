from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

# Define fields of study with descriptions and recommended courses
FIELDS_OF_STUDY = {
    "Science": {
        "description": "The systematic study of the structure and behavior of the physical and natural world.",
        "courses": {
            "Physics": "The study of matter, energy, and the forces that govern them.",
            "Biology": "The study of living organisms and their interactions.",
            "Chemistry": "The study of substances, their properties, and reactions."
        }
    },
    "Engineering": {
        "description": "The application of science and math to solve real-world problems.",
        "courses": {
            "Mechanical Engineering": "Focuses on designing and manufacturing mechanical systems.",
            "Electrical Engineering": "Deals with electrical systems, circuits, and power generation.",
            "Civil Engineering": "Concerns the design and construction of infrastructure."
        }
    }
}

# Define personalities and famous people
PERSONALITIES = {
    "Melancholic": {
        "famous_person": {"name": "Isaac Newton", "bio": "A mathematician and physicist who developed the laws of motion."},
        "image_url": "https://example.com/newton.jpg"
    },
    "Phlegmatic": {
        "famous_person": {"name": "Mahatma Gandhi", "bio": "A leader known for non-violent resistance."},
        "image_url": "https://example.com/gandhi.jpg"
    }
}

# Input model
class PersonalityInput(BaseModel):
    O_score: float
    C_score: float
    E_score: float
    A_score: float
    N_score: float

@app.post("/predict")
def predict(input_data: PersonalityInput):
    # Simulating personality breakdown (for now, random percentages)
    personality_breakdown = {
        "Melancholic": random.randint(30, 70),
        "Phlegmatic": 100 - personality_breakdown["Melancholic"]
    }

    # Select primary and secondary fields based on mock logic
    primary_field = "Science"
    secondary_field = "Engineering"

    primary_info = FIELDS_OF_STUDY[primary_field]
    secondary_info = FIELDS_OF_STUDY[secondary_field]

    # Generate LLM-based career insights (Placeholder text)
    llm_generated_text = f"People with a {primary_field} background excel in analytical thinking and problem-solving."

    # Get a famous person with a similar personality type
    personality_type = "Melancholic" if personality_breakdown["Melancholic"] > 50 else "Phlegmatic"
    famous_person = PERSONALITIES[personality_type]["famous_person"]
    image_url = PERSONALITIES[personality_type]["image_url"]

    return {
        "personality_breakdown": personality_breakdown,
        "primary_field": {"name": primary_field, "description": primary_info["description"]},
        "primary_courses": primary_info["courses"],
        "secondary_field": {"name": secondary_field, "description": secondary_info["description"]},
        "secondary_courses": secondary_info["courses"],
        "career_insights": llm_generated_text,
        "famous_person": famous_person,
        "image_url": image_url
    }