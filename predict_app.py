import joblib
import pandas as pd
from flask import Flask, request, jsonify

# 1. Create Flask app instance
app = Flask(__name__)

# 2. Load the trained pipeline
# Ensure the path is correct relative to where you run the script
# It loads the model AND the preprocessing steps
try:
    model_pipeline = joblib.load('titanic_logistic_regression_model.joblib')
    print("Model pipeline loaded successfully.")
except FileNotFoundError:
    print("Error: Model file 'titanic_logistic_regression_model.joblib' not found.")
    model_pipeline = None
except Exception as e:
    print(f"Error loading model pipeline: {e}")
    model_pipeline = None

# Define the features the model expects (matching training)
# Ensure the order matches the preprocessing steps within the pipeline
# These were: Pclass, Sex, Age, SibSp, Parch, Fare, Embarked
expected_features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']

# 3. Define the prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    """Receives passenger data in JSON, returns survival prediction."""
    if model_pipeline is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        # Get data from the POST request's JSON body
        data = request.get_json(force=True)
        print(f"Received data: {data}")

        # --- Data Preparation ---
        # Convert JSON data to a Pandas DataFrame
        # IMPORTANT: The input data structure must match what the model expects
        # We assume the input JSON keys match our feature names
        input_df = pd.DataFrame([data])

        # Ensure all expected columns are present, even if some are missing in input
        # (though for prediction, all features used in training are usually required)
        for col in expected_features:
            if col not in input_df.columns:
                # Handle missing columns if necessary (e.g., fill with default or raise error)
                # For simplicity here, we'll assume the caller sends all required fields.
                # If not, the pipeline's imputer might handle some, but structure is key.
                 print(f"Warning: Feature '{col}' missing in input data.")
                 # Consider returning an error if a required feature is missing
                 # return jsonify({"error": f"Missing feature: {col}"}), 400
                 pass # Allow pipeline's imputer to handle it if possible

        # Reorder columns to match the order expected by the preprocessor in the pipeline
        try:
             input_df = input_df[expected_features]
        except KeyError as e:
             print(f"Error: Input data missing expected feature: {e}")
             return jsonify({"error": f"Input data missing expected feature: {e}"}), 400


        print(f"Prepared DataFrame for prediction:\n{input_df}")

        # --- Prediction ---
        # Use the loaded pipeline to predict (it handles preprocessing)
        prediction = model_pipeline.predict(input_df)
        prediction_proba = model_pipeline.predict_proba(input_df) # Get probabilities

        # --- Format Response ---
        # Extract the prediction result (it's usually an array)
        prediction_result = int(prediction[0]) # Get the first element as int
        probability_class_1 = prediction_proba[0][1] # Probability of survival (class 1)

        print(f"Prediction: {prediction_result}, Probability (Survived): {probability_class_1:.4f}")

        # Return the prediction as JSON
        return jsonify({
            'prediction': prediction_result, # 0 for Not Survived, 1 for Survived
            'probability_survived': round(probability_class_1, 4)
        })

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500

# 4. Run the Flask app
if __name__ == '__main__':
    # Run on 0.0.0.0 to make it accessible from outside the container (and locally)
    # Use a standard port like 5000
    # debug=True is helpful for development (shows errors, auto-reloads)
    # but should be False in production
    app.run(host='0.0.0.0', port=5000, debug=True)