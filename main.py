from fastapi import FastAPI
import temperament_conversion
import numpy as np
from pydantic import BaseModel
from Hardcode import calculate_temperament_scores, recommend_career
from temperament_conversion import convert_temperament_to_features
import json
import joblib
import random
import requests
import os
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the Hugging Face API key
HUGGING_FACE_API_KEY = os.getenv("HF_API_KEY")

if not HUGGING_FACE_API_KEY:
    raise ValueError("Missing API key! Set HF_API_KEY in your .env file.")

model = joblib.load('modelv2_file.pkl')
scaler = joblib.load('scaler.pkl')
label_career_map = joblib.load('label_career_map.pkl')

app = FastAPI()

MODEL_NAME = "HuggingFaceH4/zephyr-7b-alpha"

def generate_career_text(prompt: str):
    """Generate AI-powered text based on the user's career personality."""
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    
    payload = {
    "inputs": prompt,
    "parameters": {"max_length": 255, "temperature": 0.7, "top_p": 0.9, "do_sample": True}
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            return result[0]["generated_text"]

    return "AI generation failed. Please try again."

def load_success_stories():
    """Load success stories from JSON file."""
    try:
        with open("success_stories.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def get_random_success_stories(dominant, secondary, success_stories, count=5):
    key = f"{dominant.title()}-{secondary.title()}"
    if key in success_stories and success_stories[key]:
        return random.sample(success_stories[key], min(count, len(success_stories[key])))
    return []

def clean_generated_text(text):
    """Remove the hardcoded intro and start from 'Let's dive deeper...'"""
    keyword = "Let us dive deeper"
    index = text.find(keyword)
    if index != -1:
        return text[index:]  # Return everything from "Let's dive deeper..."
    return text  # Return original if keyword isn't found

temperament_desription = {
    "dominant": {
    "melancholy": "Depth, introspection, and a relentless pursuit of meaning—that’s you. Your mind operates on a different wavelength, analyzing, perfecting, and seeking deeper truths. You see what others miss, making you an idealist, strategist, and thinker.",
    "sanguine": "You're a natural charmer—radiant, adventurous, and effortlessly social. People gravitate toward your energy, and you thrive in fast-paced, exciting environments. Whether leading a conversation or lighting up a room, your presence is impossible to ignore.",
    "choleric": "You’re unstoppable—driven, strategic, and born to take charge. Challenges excite you, and you never back down from competition. Your mind is wired for problem-solving and leadership, always pushing forward with confidence and intensity.",
    "phlegmatic": "You're calm, wise, and effortlessly cool—the person everyone trusts. Where others rush, you reflect. You excel at understanding people, keeping peace, and bringing stability wherever you go. Your presence is soothing, yet your wisdom runs deep."
    },
    "secondary": {
    "melancholy": "Your Melancholic side adds a layer of depth, focus, and high standards to your personality. While others may be content with the surface, you refine, improve, and seek mastery. It gives you a thoughtful, artistic, or intellectual streak that sets you apart.",
    "sanguine": "You add a vibrant spark to everything you do. While your core temperament may lean more serious or structured, your Sanguine side keeps things light and engaging. You bring warmth, humor, and adaptability, making you a breath of fresh air in any situation.",
    "choleric": "Your Choleric edge makes you more decisive, ambitious, and fearless than others with your core temperament. You’re not just content with dreams—you take action. You bring strength and clarity to your pursuits, ensuring you stand out.",
    "phlegmatic": "Your Phlegmatic side gives you a calm and adaptable nature, balancing out any intensity from your core temperament. It makes you diplomatic, easygoing, and reliable, ensuring you’re a grounding force in any situation."
    },
}

temperament_blend_descriptions = {
    "melancholy-sanguine": {
        "shorthand": "MelSan",
        "description": "You are a fascinating mix of deep introspection and vibrant energy. While your Melancholy side seeks depth, meaning, and perfection, your Sanguine side brings warmth, charm, and a love for adventure. This makes you both analytical and expressive—a thinker who also knows how to captivate a room. You balance reflection with spontaneity, making you a deep conversationalist who can switch between serious discussions and lighthearted fun effortlessly."
    },
    
    "melancholy-choleric": {
        "shorthand": "MelChlor",
        "description": "Intensely driven and deeply analytical, you are a powerhouse of intellect and ambition. Your Melancholy side ensures you think critically and strive for mastery, while your Choleric nature pushes you to take action and lead. You combine deep thought with strategic execution, making you a force to be reckoned with in any field. While you may have high standards for yourself and others, your ability to both analyze and take charge gives you a unique edge in leadership and problem-solving."
    },
    
    "melancholy-phlegmatic": {
        "shorthand": "MelPhleg",
        "description": "A deep thinker with a calm presence, you blend insight with emotional intelligence. Your Melancholy side makes you analytical and idealistic, while your Phlegmatic nature adds patience, diplomacy, and emotional depth. This means you can navigate complex thoughts and emotions effortlessly. You’re reflective yet approachable, making you an excellent mediator, counselor, or strategist. Your wisdom is both intellectual and emotional, allowing you to bring stability wherever you go."
    },
    
    "sanguine-melancholy": {
        "shorthand": "SanMel",
        "description": "You’re a rare combination of lighthearted joy and deep reflection. Your Sanguine side is charming, energetic, and loves people, while your Melancholy side craves meaning, artistry, and perfection. This blend makes you a passionate storyteller, artist, or communicator. You can engage people with enthusiasm while also offering deep insights. Though you love excitement, you also need moments of solitude to process emotions and ideas before re-engaging with the world."
    },
    
    "sanguine-choleric": {
        "shorthand": "SanChlor",
        "description": "A bold, high-energy leader, you thrive in dynamic environments. Your Sanguine side makes you social, optimistic, and adaptable, while your Choleric nature adds ambition, decisiveness, and drive. This makes you a natural leader—someone who can inspire and take charge simultaneously. You’re both persuasive and strategic, able to rally people to your cause while executing your plans with confidence. However, your high energy means you may need to slow down and reflect at times."
    },
    
    "sanguine-phlegmatic": {
        "shorthand": "SanPhleg",
        "description": "You’re effortlessly charming, easygoing, and people-oriented. Your Sanguine side brings joy, enthusiasm, and sociability, while your Phlegmatic nature adds patience, adaptability, and a laid-back attitude. This makes you the ultimate people person—someone who connects with others effortlessly and keeps the peace. You can navigate social settings with ease, making you a great communicator, counselor, or entertainer. While you enjoy fun and excitement, you also know how to stay grounded."
    },
    
    "choleric-melancholy": {
        "shorthand": "ChlorMel",
        "description": "A relentless perfectionist and strategist, you combine the best of ambition and intellect. Your Choleric side gives you the drive to lead and conquer challenges, while your Melancholy nature ensures that you analyze every step with precision. This makes you a formidable problem-solver—someone who doesn’t just act, but acts with purpose and strategy. You have high expectations for yourself and others, and while you may seem intense, your depth of thought ensures that your leadership is well-founded."
    },
    
    "choleric-sanguine": {
        "shorthand": "ChlorSan",
        "description": "Fearless, persuasive, and full of life, you are a force of nature. Your Choleric side makes you ambitious and determined, while your Sanguine energy ensures you remain charismatic and adaptable. You have a magnetic personality, drawing people toward your vision while maintaining the confidence to push forward. You thrive in leadership roles, sales, or any position where influence and action matter. Though you love being in control, your charm ensures that people willingly follow your lead."
    },
    
    "choleric-phlegmatic": {
        "shorthand": "ChlorPhleg",
        "description": "A unique mix of drive and patience, you are both a leader and a steady force. Your Choleric side makes you goal-oriented and determined, while your Phlegmatic nature gives you the ability to remain calm under pressure. This means you can command respect without being overly aggressive—you have the ambition to push forward but the wisdom to pick your battles carefully. You’re the kind of leader who doesn’t just demand authority but earns it through consistency and reliability."
    },
    
    "phlegmatic-melancholy": {
        "shorthand": "PhlegMel",
        "description": "A quiet yet profound thinker, you bring both emotional depth and intellectual insight to the table. Your Phlegmatic side makes you patient and diplomatic, while your Melancholy nature ensures you analyze situations deeply. You prefer to work behind the scenes, offering wisdom and stability to those around you. You are naturally drawn to roles that require deep reflection, such as writing, counseling, or philosophy. Though you may not seek the spotlight, your insight shapes those who listen."
    },
    
    "phlegmatic-sanguine": {
        "shorthand": "PhlegSan",
        "description": "Warm, easygoing, and socially gifted, you make people feel comfortable and valued. Your Phlegmatic side keeps you calm and reliable, while your Sanguine nature adds a fun, engaging spark. This makes you an excellent friend, mentor, or team player—someone who can balance lightheartedness with stability. You enjoy social interactions but don’t need to be the center of attention. Instead, you bring harmony and connection to groups, making you an essential part of any team or community."
    },
    
    "phlegmatic-choleric": {
        "shorthand": "PhlegChlor",
        "description": "A rare combination of patience and determination, you are both steady and goal-driven. Your Phlegmatic side makes you relaxed and easygoing, but your Choleric nature ensures you don’t back down from challenges. This means you have an inner drive to succeed without the need for aggression. You can lead without being forceful and influence without being overbearing. People trust you because of your calm yet determined nature, making you a natural in leadership, negotiation, and strategic planning."
    }
}

def ml_model_processing(input):
    try:
        # Convert input data to numpy array and reshape for model
        features = np.array([[input["O_score"], input["C_score"], input["E_score"], input["A_score"], input["N_score"]]])

        # Standardize features
        features_scaled = scaler.transform(features)

        # Make prediction
        predicted_category = model.predict(features_scaled)[0]

        # Convert label to career category
        career_category = label_career_map.get(predicted_category, "Unknown")

        return {"career_category": career_category}

    except Exception as e:
        return {"error": str(e)}

class PersonalityInput(BaseModel):
    melancholy: list
    sanguine: list
    choleric: list
    phlegmatic: list

@app.post("/predict")
def predict(input_data: PersonalityInput):
    responses = input_data.dict()

    # Step 1: Calculate Temperament Scores
    dominant, dominant_percentage, secondary, secondary_percentage = calculate_temperament_scores(responses)

    # Step 2: Determine Dominant and Secondary Temperaments
    dominant_percentage = round(dominant_percentage / 100, 2)
    secondary_percentage = round(secondary_percentage / 100, 2)

    # Step 3: Recommend Career Paths
    recommendations = recommend_career(dominant, dominant_percentage, secondary, secondary_percentage)
    ml_features = convert_temperament_to_features(responses["melancholy"], responses["sanguine"], responses["phlegmatic"], responses["choleric"])
    ml_career = ml_model_processing(ml_features) or {"career_category": "General Studies"}

    # Step 4: Generate AI-powered career description
    primary_field = recommendations["primary"]["fieldOfStudy"]["name"]
    secondary_field = recommendations["secondary"]["fieldOfStudy"]["name"]

    primary_courses = [course["name"] for course in recommendations["primary"]["courseOfStudy"]]
    secondary_courses = [course["name"] for course in recommendations["secondary"]["courseOfStudy"]]

    career_prompt = (
        f"You have a {dominant} temperament with a {secondary} influence, which makes you naturally suited for "
        f"these fields: {primary_field} (primary) and {secondary_field} (secondary). "
        f"Here’s why you’ll thrive in them: "
    )

    if primary_courses:
        career_prompt += f"In {primary_field}, you might enjoy courses like {', '.join(primary_courses)}. "

    if secondary_courses:
        career_prompt += f"In {secondary_field}, you could explore {', '.join(secondary_courses)}. "
    
    career_prompt += (
    "You thrive in these areas because of your unique blend of qualities. "
    "Let us dive deeper into why these fields are a perfect fit for you."
    )

    career_text = generate_career_text(career_prompt)
    career_text = career_text.replace("This person", "You").replace("They are", "You are").replace("They have", "You have")
    career_text = clean_generated_text(career_text)
    
    success_stories = load_success_stories()
    success_story = get_random_success_stories(dominant, secondary, success_stories)


    # Step 5: Generate API Response
    return {
        "temperaments": [
            {"name": dominant, "percentage": dominant_percentage, "description": temperament_desription["dominant"][dominant]},
            {"name": secondary, "percentage": secondary_percentage, "description": temperament_desription["secondary"][secondary]}
        ],
        "recommendations": recommendations,
        "successStories": success_story if success_story else [],
        "youAndYourCareer": career_text,
        "temperament-blend": {"name": temperament_blend_descriptions[f"{dominant}-{secondary}"]["shorthand"], "description": temperament_blend_descriptions[f"{dominant}-{secondary}"]["description"]}
    }

# TODO: convince Lekan to change it to melancholic not melancholy. Don't forget to alter both success_stories files and hardcode files
# TODO: Ensure consistency in ordering of the temperaments
# TODO: Integrate ml_field properly (honestly just ask him how he wants it, because there is no sitution where his solution will never show)
