# from flask import Flask, request, jsonify
# from .algorithms.temperament_logic import calculate_temperament, determine_dominant_temperaments, recommend_fields

# app = Flask(__name__)

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.get_json() 
#     # Extract relevant data from the request (e.g., personality scores)
#     responses = data.get('personality_scores') 

#     # Call your algorithm 
#     temperaments = calculate_temperament(responses)
#     dominant, secondary, dominant_percentage, secondary_percentage = determine_dominant_temperaments(temperaments)
#     recommended_fields = recommend_fields(dominant, secondary, dominant_percentage, secondary_percentage)

#     return jsonify({
#                     "Temperament Scores": temperaments,
#                     "Dominant Temperament": [dominant, dominant_percentage],
#                     "Secondary Temperament": [secondary, secondary_percentage],
#                     "Recommended Fields": recommended_fields
#                     })

# if __name__ == '__main__':
#     app.run(debug=True)