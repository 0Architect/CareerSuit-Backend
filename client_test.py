import numpy as np
import joblib

def map_to_temperament(O, C, E, A, N):
    if E > 0.6 and N < 0.4:
        return "Sanguine" #0
    elif E < 0.4 and N > 0.6:
        return "Melancholic" #1
    elif E > 0.6 and C > 0.6:
        return "Choleric" #2
    elif E < 0.4 and A > 0.6:
        return "Phlegmatic" #3
    else:
        return "Balanced" #4
# Load model
model = joblib.load('model_file.pkl')

# Prepare new input data (OCEAN scores + Temperament)
new_data = np.array([[0.5, 0.6, 0.7, 0.8, 0.3, 1]])  # Example values for OCEAN + Temperament

# Predict career category
prediction = model.predict(new_data)
career_categories = ['Science', 'Social Science', 'Entrepreneurship', 'Art', 'Medicine', 'Engineering']
print("Predicted Career:", career_categories[prediction[0]])