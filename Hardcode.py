import random

def calculate_temperament_scores(scores):
    """
    Convert raw temperament scores into percentages for primary and secondary temperaments.
    """
    # Sum only values that are 4 or 5 for each temperament
    filtered_scores = {k: sum(val for val in values if val >= 4) for k, values in scores.items()}
    
    if not any(filtered_scores.values()):
        filtered_scores = {k: sum(val for val in values if val >= 3) for k, values in scores.items()}
        raise ValueError("Invalid scores")
    
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
        {"name": "Biology", "description": "The study of living organisms and their interactions."},
        {"name": "Chemistry", "description": "The study of substances, their properties, and reactions."},
        {"name": "Physics", "description": "The study of matter, energy, and the fundamental forces of nature."},
        {"name": "Computer Science", "description": "The study of computation, algorithms, and information processing."},
        {"name": "Astronomy", "description": "The study of celestial objects and phenomena beyond Earth."},
        {"name": "Engineering", "description": "The application of scientific and mathematical principles to design and build structures, machines, and systems."}
    ],
    "Medicine": [
        {"name": "Medicine", "description": "The science and practice of diagnosing, treating, and preventing diseases."},
        {"name": "Biotechnology", "description": "The use of biological systems and organisms to develop new technologies and products."},
        {"name": "Pharmacology", "description": "The study of drugs, their effects, and their interactions in living organisms."},
        {"name": "Neuroscience", "description": "The study of the nervous system and brain function."},
        {"name": "Public Health", "description": "The science of protecting and improving the health of communities through education, research, and policy."}
    ],
    "Social Sciences": [
        {"name": "Psychology", "description": "The study of human behavior and mental processes."},
        {"name": "Political Science", "description": "The study of government systems, political behavior, and public policies."},
        {"name": "Economics", "description": "The study of production, distribution, and consumption of goods and services."},
        {"name": "Sociology", "description": "The study of social behavior, institutions, and human interactions."},
        {"name": "Law", "description": "The study of legal systems, justice, and governance."}
    ],
    "Arts": [
        {"name": "Film and Media Studies", "description": "The study of film, television, and digital media, including their production and cultural impact."},
        {"name": "Fashion Design", "description": "The art of creating clothing and accessories based on aesthetics and functionality."},
        {"name": "Music", "description": "The study and practice of musical composition, theory, and performance."},
        {"name": "Animation and Visual Effects", "description": "The creation of digital animations and visual storytelling using technology."},
        {"name": "Industrial Design", "description": "The process of designing consumer products for functionality and aesthetics."}
    ],
    "Entrepreneurship": [
        {"name": "Business Administration", "description": "The management and operation of businesses, including strategy and decision-making."},
        {"name": "Finance", "description": "The management of investments, assets, and financial markets."},
        {"name": "Marketing", "description": "The study of consumer behavior and strategies to promote products and services."},
        {"name": "International Business", "description": "The study of global markets, trade policies, and multinational business strategies."},
        {"name": "Investment Banking", "description": "The financial service of advising corporations and governments on raising capital and financial transactions."}
    ]
}

non_demanding_courses = {
     "Sciences": [
            {"name": "General Science", "description": "A broad study of fundamental scientific principles."},
            {"name": "Environmental Science", "description": "Studying ecosystems, sustainability, and conservation."},
            {"name": "Botany", "description": "The study of plants, their structures, and their functions."},
            {"name": "Zoology", "description": "Exploring animal biology, behavior, and habitats."},
            {"name": "Geology", "description": "Studying Earth's physical characteristics, from geology to weather patterns."}
        ],
        "Social Sciences": [
            {"name": "Sociology", "description": "Analyzing human societies, cultures, and social interactions."},
            {"name": "Cultural Studies", "description": "Exploring traditions, identities, and global cultural diversity."},
            {"name": "Anthropology", "description": "Studying human evolution, customs, and civilizations."},
            {"name": "Peace and Conflict Studies", "description": "Understanding global conflicts and peacekeeping strategies."},
            {"name": "Communication Studies", "description": "Examining how people share information across different media and contexts."}
        ],
        "Arts": [
            {"name": "Graphic Design", "description": "Creating visual content using artistic and digital techniques."},
            {"name": "Creative Writing", "description": "Crafting stories, poetry, and other literary works."},
            {"name": "Photography", "description": "Capturing and editing images professionally."},
            {"name": "Film Studies", "description": "Analyzing movies, genres, and directors from a theoretical perspective rather than production or technical skills."},
            {"name": "Interior Design", "description": "Designing indoor spaces for functionality and aesthetics."}
        ],
        "Entrepreneurship": [
            {"name": "Small Business Management", "description": "Running and operating small-scale enterprises."},
            {"name": "Business Communication", "description": "Focuses on effective writing, presentations, and professional communication in a business setting."},
            {"name": "Retail Management", "description": "Overseeing sales and store operations."},
            {"name": "Public Relations", "description": "Managing company image and communications."},
            {"name": "Event Planning", "description": "Organizing and managing events and gatherings."}
        ],
    # Will never be called
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
    if primary == "melancholy" and primary_percentage >= 40:
        primary_field = "Sciences"
    # If dominant is melancholy and secondary is phlegmatic with >45% on melancholy, recommend Medicine.
    if primary == "melancholy" and secondary == "phlegmatic" and primary_percentage >= 45:
        primary_field = "Medicine"
    # If sanguine is dominant (>50%), recommend Entrepreneurship.
    if primary == "sanguine" and primary_percentage > 50:
        primary_field = "Entrepreneurship"
    # If the combination is choleric and phlegmatic, recommend Entrepreneurship.
    if primary in {"choleric", "sanguine"} and secondary in {"choleric", "sanguine"}:
        primary_field = "Entrepreneurship"

    # Adjust based on the percentage ranges:
    if 71 <= primary_percentage <= 90:
        # Strong dominance: only primary is recommended.
        # For secondary, we default to the same field but with only non-demanding courses.
        secondary_field = primary_field
        secondary_demanding = False
    elif 65 <= primary_percentage and primary in {"choleric", "sanguine"}:
        # For these extroverted types, do not choose demanding courses in the secondary field.
        secondary_demanding = False
    elif 51 <= primary_percentage <= 60:
        # Both fields should use non-demanding course options.
        primary_demanding = True
        secondary_demanding = True
    elif secondary_percentage <= 35 and primary in {"choleric", "melancholy"}:
        secondary_demanding = True
    elif primary == "choleric" and primary_percentage >= 62:
        primary_field = "Entrepreneurship"

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
