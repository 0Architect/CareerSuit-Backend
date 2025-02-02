import pandas as pd
import lightgbm as lgb
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("Data_final.csv")

# Define Four Temperaments mapping
def map_to_temperament(O, C, E, A, N):
    if E > 0.6 and N < 0.4:
        return "Sanguine"
    elif E < 0.4 and N > 0.6:
        return "Melancholic"
    elif E > 0.6 and C > 0.6:
        return "Choleric"
    elif E < 0.4 and A > 0.6:
        return "Phlegmatic"
    else:
        return "Balanced"

# Apply temperament mapping
df["Temperament"] = df.apply(lambda row: map_to_temperament(row.O_score, row.C_score, row.E_score, row.A_score, row.N_score), axis=1)

# Encode Temperament
encoder_temperament = LabelEncoder()
df["Temperament"] = encoder_temperament.fit_transform(df["Temperament"])

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
                    "Software Quality Assurance Tester", "Database Analyst", "Electronics Design Engineer"]
}

# Apply career grouping
def map_career_to_category(career):
    for category, careers in CAREER_GROUPS.items():
        if career in careers:
            return category
    return "Other"  # Catch any unmapped careers

df["Career_Category"] = df["Career"].apply(map_career_to_category)

# Encode Career Categories
encoder_career = LabelEncoder()
df["Career_Category"] = encoder_career.fit_transform(df["Career_Category"])

# Feature selection (Only OCEAN + Temperament)
X = df[["O_score", "C_score", "E_score", "A_score", "N_score", "Temperament"]]
y = df["Career_Category"]

# Check class distribution
sns.countplot(x=y)
plt.xticks(rotation=90)
plt.title("Career Category Distribution")
plt.show()

# Train-test split (ensures all categories have representation)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Train LightGBM model with optimized settings
model = lgb.LGBMClassifier(n_estimators=500, max_depth=10, learning_rate=0.05)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = (y_pred == y_test).mean()
print("ML Model Accuracy:", accuracy)

# Feature Importance
lgb.plot_importance(model, max_num_features=10)
plt.show()

joblib.dump(model, 'model_file.pkl')