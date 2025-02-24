import random

def calculate_temperament_scores(scores):
    """
    Convert raw temperament scores into percentages for primary and secondary temperaments.
    Only values of 4 and 5 are considered.
    """
    # Sum only values that are 4 or 5 for each temperament
    filtered_scores = {k: sum(val for val in values if val >= 4) for k, values in scores.items()}
    
    if not any(filtered_scores.values()):
        raise ValueError("Invalid scores: No temperament has a valid score (4 or 5).")
    
    # Sort temperaments by their filtered score (highest first)
    sorted_temperaments = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)
    primary, secondary = sorted_temperaments[:2]
    total = primary[1] + secondary[1]
    
    primary_percentage = (primary[1] / total) * 100
    secondary_percentage = (secondary[1] / total) * 100
    
    return primary[0], primary_percentage, secondary[0], secondary_percentage

def determine_extroversion(primary, secondary, percentage):
    """
    If there is a 50-50 split and one of the two temperaments is extroverted,
    return the extroverted temperament.
    """
    extroverts = {"sanguine", "choleric"}
    if percentage == 50 and {primary, secondary} & extroverts:
        return primary if primary in extroverts else secondary
    return primary

def closest_temperament(temperament):
    """Return the closest temperament for a 100% case."""
    closest = {
        "melancholy": "phlegmatic", 
        "phlegmatic": "melancholy",
        "sanguine": "choleric",
        "choleric": "sanguine"
    }
    return closest[temperament]

# Dictionaries for courses (feel free to modify these lists as needed)
demanding_courses = {
    "Sciences": [
        {"name": "Theoretical Physics", "description": "Exploring the fundamental laws of the universe."},
        {"name": "Molecular Chemistry", "description": "Studying chemical interactions at the molecular level."},
        {"name": "Electrical Engineering", "description": "Designing and analyzing electrical systems."},
        {"name": "Mechanical Engineering", "description": "Designing, analyzing, and manufacturing mechanical systems."},
        {"name": "Civil Engineering", "description": "Planning and constructing infrastructure projects like roads and bridges."},
        {"name": "Architecture", "description": "Designing and constructing buildings and structures."}
    ],
    "Social Sciences": [
        {"name": "Economics", "description": "Analyzing financial systems and economic policies."},
        {"name": "Accounting", "description": "Managing financial records and ensuring regulatory compliance."},
        {"name": "Finance", "description": "Analyzing investments, assets, and financial markets."},
        {"name": "Political Science", "description": "The study of government systems, political behavior, and the impact of policies on society."},
        {"name": "Law", "description": "Understanding and applying legal principles in governance and justice."},
    ],
    "Arts": [
        {"name": "Film Directing", "description": "Bringing creative vision to life in cinematic productions."},
        {"name": "Fashion Design", "description": "Fashion Design is the art of creating clothing and accessories by combining creativity, textiles, and trends to develop functional and aesthetic styles."},
        {"name": "Music Composition and Production", "description": "Involves music theory, instrumentation, recording techniques, and digital sound production, requiring both creativity and technical skill."},
        {"name": "Animation and Visual Effects", "description": "Combines artistic creativity with technical mastery of digital tools, requiring expertise in software like Maya, Blender, or After Effects."},
        {"name": "Industrial Design", "description": "Focuses on designing functional products with an emphasis on aesthetics, usability, and manufacturing processes, requiring both creativity and engineering knowledge."}
    ],
    "Entrepreneurship": [
        {"name": "Financial Engineering", "description": "Applies mathematical models to develop financial instruments and manage risk, involving complex quantitative analysis."},
        {"name": "Actuarial Science", "description": "Uses mathematics, statistics, and financial theory to assess risk in insurance and finance, requiring extensive exams and certifications."},
        {"name": "Business Law", "description": "Covers corporate regulations, contract law, and legal frameworks affecting businesses, requiring a strong grasp of legal principles."},
        {"name": "International Business", "description": "Studies global markets, trade policies, and multinational business strategies, demanding knowledge of economics, law, and finance."},
        {"name": "Investment Banking", "description": "Investment Banking is the financial service of advising corporations and governments on raising capital, mergers, acquisitions, and complex financial transactions."},
    ],
    "Medicine": [
        {"name": "Neurosurgery", "description": "Performing complex surgeries on the brain and nervous system."},
        {"name": "Cardiothoracic Surgery", "description": "Focuses on surgical procedures involving the heart, lungs, and chest cavity, demanding precision and extensive knowledge of human anatomy"},
        {"name": "Orthopedic Surgery", "description": "Involves treating bone and muscle disorders through complex surgical interventions and rehabilitation."},
        {"name": "General Surgery", "description": "Covers a broad range of surgical procedures on various organs, requiring mastery of anatomy and surgical techniques."},
        {"name": "Oncology", "description": "Involves diagnosing and treating cancer, requiring deep knowledge of pathology, chemotherapy, and advanced treatment methods."},
    ]
}

non_demanding_courses = {
    "Sciences": [
        {"name": "General Science", "description": "A broad study of fundamental scientific principles."},
        {"name": "Environmental Science", "description": "Studying ecosystems, sustainability, and conservation."},
        {"name": "Botany", "description": "The study of plants, their structures, and their functions."},
        {"name": "Zoology", "description": "Exploring animal biology, behavior, and habitats."},
        {"name": "Microbiology basics", "description": "Studying microscopic organisms and their roles in nature."}
    ],
    "Social Sciences": [
        {"name": "Sociology", "description": "Analyzing human societies, cultures, and social interactions."},
        {"name": "Cultural Studies", "description": "Exploring traditions, identities, and global cultural diversity."},
        {"name": "Anthropology", "description": "Studying human evolution, customs, and civilizations."},
        {"name": "Peace and Conflict Studies", "description": "Understanding global conflicts and peacekeeping strategies."},
        {"name": "Gender Studies", "description": "Exploring gender roles, identity, and social equality."}
    ],
    "Arts": [
        {"name": "Graphic Design", "description": "Creating visual content using artistic and digital techniques."},
        {"name": "Creative Writing", "description": "Crafting stories, poetry, and other literary works."},
        {"name": "Photography", "description": "Capturing and editing images professionally."},
        {"name": "Film Studies", "description": "Analyzes movies, genres, and directors from a theoretical perspective rather than production or technical skills."},
        {"name": "Interior Design", "description": "Designing indoor spaces for functionality and aesthetics."}
    ],
    "Entrepreneurship": [
        {"name": "Small Business Management", "description": "Running and operating small-scale enterprises."},
        {"name": "Business Communication", "description": "Focuses on effective writing, presentations, and professional communication in a business setting."},
        {"name": "Retail Management", "description": "Overseeing sales and store operations."},
        {"name": "Public Relations", "description": "Managing company image and communications."},
        {"name": "Event Planning", "description": "Organizing and managing events and gatherings."}
    ],
    "Medicine": [
        {"name": "Medical Ethics", "description": "Explores moral principles in medicine, including patient rights and healthcare laws."},
        {"name": "Public Health", "description": "Focuses on disease prevention, health promotion, and community health management."},
        {"name": "Health and Wellness Studies", "description": "Covers general well-being, nutrition, mental health, and fitness with minimal technical depth."},
        {"name": "Medical Sociology", "description": "Examines the social aspects of health, illness, and the healthcare system."},
        {"name": "First Aid and Basic Life Support", "description": "Teaches emergency response techniques like CPR and wound care, without deep medical theory."}
    ]
}

def determine_fields(primary, primary_percentage, secondary, secondary_percentage):
    """
    Based on the temperament percentages and given conditions, determine:
      - the primary field recommendation
      - the secondary field recommendation
      - whether the recommended courses for each field should be from the demanding or non-demanding set.
    """
    # Default mapping from temperament to field
    default_field_map = {
        "melancholy": "Sciences",
        "sanguine": "Arts",
        "choleric": "Social Sciences",
        "phlegmatic": "Social Sciences"
    }
    
    # Start with defaults based on temperament
    primary_field = default_field_map[primary]
    secondary_field = default_field_map[secondary]
    
    # Flags to choose between demanding or non-demanding courses
    primary_demanding = True
    secondary_demanding = True

    # Specific overrides based on instructions:
    # If melancholy is dominant (>40%), engineering fields (within Sciences) might work.
    if primary == "melancholy" and primary_percentage > 40:
        primary_field = "Sciences"
    # If dominant is melancholy and secondary is phlegmatic with >45% on melancholy, recommend Medicine.
    if primary == "melancholy" and secondary == "phlegmatic" and primary_percentage > 45:
        primary_field = "Medicine"
    # If sanguine is dominant (>50%), recommend Entrepreneurship.
    if primary == "sanguine" and primary_percentage > 50:
        primary_field = "Entrepreneurship"
    # If the combination is choleric and phlegmatic, recommend Entrepreneurship.
    if {primary, secondary} == {"choleric", "phlegmatic"}:
        primary_field = "Entrepreneurship"

    # Adjust based on the percentage ranges:
    if 71 <= primary_percentage <= 90:
        # Strong dominance: only primary is recommended.
        # For secondary, we default to the same field but with only non-demanding courses.
        secondary_field = primary_field
        secondary_demanding = False
    elif 66 <= primary_percentage <= 71 and primary in {"choleric", "sanguine"}:
        # For these extroverted types, do not choose demanding courses in the secondary field.
        secondary_demanding = False
    elif 51 <= primary_percentage <= 60:
        # Both fields should use non-demanding course options.
        primary_demanding = False
        secondary_demanding = False

    return primary_field, primary_demanding, secondary_field, secondary_demanding

def recommend_career(primary, primary_percentage, secondary, secondary_percentage):
    """
    Using the temperament scores and percentages, determine the recommended fields
    and provide a dictionary with two keys (primary and secondary fields), each mapping
    to course recommendations (separated into demanding and non-demanding lists).
    """
    # Handle 100% case: if primary_percentage is 100, split 50-50 with the closest temperament.
    if primary_percentage == 100:
        secondary = closest_temperament(primary)
        primary_percentage = secondary_percentage = 50

    # Determine the recommended fields and whether each should pull from demanding courses.
    primary_field, primary_demanding, secondary_field, secondary_demanding = determine_fields(
        primary, primary_percentage, secondary, secondary_percentage
    )

    # Build the recommendation dictionary.
    recommendation = {
        "primary": {
            "fieldOfStudy": {
                "name": primary_field,
                "description": "Best fit based on temperament."
            },
            "courseOfStudy": list(
                [{"name": course["name"], "description": course["description"]} for course in demanding_courses.get(primary_field, []) if primary_demanding] +
                [{"name": course["name"], "description": course["description"]} for course in non_demanding_courses.get(primary_field, [])]
            )[:5]
        },
        "secondary": {
            "fieldOfStudy": {
                "name": secondary_field if secondary_field else "None",
                "description": "Alternate field based on temperament."
            },
            "courseOfStudy": list(
                [{"name": course["name"], "description": course["description"]} for course in demanding_courses.get(secondary_field, []) if secondary_demanding] +
                [{"name": course["name"], "description": course["description"]} for course in non_demanding_courses.get(secondary_field, [])]
            )[:5]
        }
    }
    return recommendation
