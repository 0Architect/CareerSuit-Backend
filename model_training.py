import pandas as pd
import lightgbm as lgb
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE

# Load dataset
df = pd.read_csv("Data_final.csv")

# Career Group Mapping
CAREER_GROUPS = {
    "Science": ["Research Scientist", "Astronomer", "Biologist", "Environmental Scientist", 
                 "Biomedical Engineer", "Zoologist", "Forensic Scientist", "Geologist", "Wildlife Biologist", 
                 "Marine Biologist", "Genetic Counselor", "Biomedical Researcher"],
    
    "Social Science": ["Psychologist", "Human Resources Manager", "Journalist", "Social Worker", 
                        "Marriage Counselor", "Public Relations Specialist", "Occupational Therapist",
                        "Forensic Psychologist", "Diplomat", "Foreign Service Officer", "Human Rights Lawyer"],
    
    "Entrepreneurship": ["Marketing Manager", "Salesperson", "Event Planner", "Real Estate Agent", 
                          "IT Project Manager", "Investment Banker", "Product Manager", "Advertising Executive",
                          "Fashion Stylist", "Marketing Copywriter"],
    
    "Art": ["Graphic Designer", "Artist", "Musician", "Film Director", "Fashion Designer", 
             "Video Game Tester", "Game Developer", "Marketing Coordinator"],
    
    "Medicine": ["Nurse", "Physician", "Pharmacist", "Physical Therapist", "Pediatrician", 
                  "Speech Therapist", "Chiropractor", "Dental Hygienist", "Radiologic Technologist",
                  "Rehabilitation Counselor"],
    
    "Engineering": ["Software Developer", "Mechanical Engineer", "Electrical Engineer", "Aerospace Engineer", 
                     "Civil Engineer", "Industrial Engineer", "Robotics Engineer", "Database Administrator",
                     "IT Support Specialist", "Web Developer", "Urban Planner", "Mechanical Designer",
                     "Software Quality Assurance Tester", "Database Analyst", "Electronics Design Engineer"],
    
    "Other": ["Accountant", "Police Officer", "Administrative Officer", "Tax Collector", "Foreign Service Officer",
               "Customs and Border Protection Officer", "Construction Engineer", "Tax Accountant", "Financial Analyst",
               "Financial Planner", "Financial Auditor", "Insurance Underwriter", "Airline Pilot", "Air Traffic Controller"]
}

# Apply career grouping
def map_career_to_category(career):
    for category, careers in CAREER_GROUPS.items():
        if career in careers:
            return category
    return "Other"  # Default fallback

df["Career_Category"] = df["Career"].apply(map_career_to_category)

# Encode Career Categories
encoder_career = LabelEncoder()
df["Career_Category"] = encoder_career.fit_transform(df["Career_Category"])

# Save mapping for later use
career_label_map = dict(zip(encoder_career.classes_, range(len(encoder_career.classes_))))
label_career_map = {v: k for k, v in career_label_map.items()}

# Feature selection (Using OCEAN scores only, removing Aptitude Scores)
FEATURES = ["O_score", "C_score", "E_score", "A_score", "N_score"]
X = df[FEATURES]
y = df["Career_Category"]

# Standardize features for better model performance
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Address class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, stratify=y_resampled, random_state=42)

# Train optimized LightGBM model
model = lgb.LGBMClassifier(n_estimators=500, max_depth=7, learning_rate=0.05, class_weight="balanced")
model.fit(X_train, y_train)

# Evaluate model using cross-validation
cv_scores = cross_val_score(model, X_resampled, y_resampled, cv=5)
print("Cross-validation accuracy:", cv_scores.mean())

# Save model and preprocessing objects
joblib.dump(model, 'modelv2_file.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_career_map, 'label_career_map.pkl')

#TODO: Link with the main API
#TODO: Retrain but remove 'other'