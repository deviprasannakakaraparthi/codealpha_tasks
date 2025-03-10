from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load Model & Scaler
with open("titanic_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Convert input data into an array
        user_input = np.array([[data["Pclass"], data["Sex"], data["Age"], data["FamilySize"], 
                                data["Fare"], data["Embarked_C"], data["Embarked_Q"], data["Embarked_S"]]])

        user_input = scaler.transform(user_input)
        prediction = model.predict(user_input)
        probability = model.predict_proba(user_input)[0][1] * 100

        return jsonify({"survived": int(prediction[0]), "probability": round(probability, 2)})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
