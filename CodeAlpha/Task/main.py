import streamlit as st
import requests
import pickle

# Set up Streamlit page config
st.set_page_config(page_title="Titanic Survival Prediction", page_icon="🚢", layout="centered")

# 🔹 Apply Background Image
st.markdown(
    """
    <style>
    .stApp {
        background: url("https://media.istockphoto.com/id/172177645/photo/the-zenobia-wreck-cyprus.webp?a=1&b=1&s=612x612&w=0&k=20&c=LLdP4-Mn8FZV52sv_E5j1iBNaOQcNHiQUds-CNUxv2g=") no-repeat center center fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 Improve Button Style
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #FF5733;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        padding: 10px;
        width: 200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 Improve Fonts
st.markdown(
    """
    <style>
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
        color: red;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title
st.title("🚢 Titanic Survival Prediction")
st.subheader("Will you survive the Titanic disaster? Let's find out!")

# User Input Fields
pclass = st.selectbox("Passenger Class (Pclass)", [1, 2, 3])
sex = st.selectbox("Sex", ["Male", "Female"])
age = st.number_input("Age", min_value=0, max_value=100, value=30)
family_size = st.number_input("Family Size", min_value=0, max_value=10, value=0)
fare = st.number_input("Fare Amount", min_value=0.0, max_value=500.0, value=50.0)
embarked = st.selectbox("Port of Embarkation", ["C", "Q", "S"])

# Convert Inputs
sex = 1 if sex == "Male" else 0
embarked_C = 1 if embarked == "C" else 0
embarked_Q = 1 if embarked == "Q" else 0
embarked_S = 1 if embarked == "S" else 0

# Predict Button
if st.button("Predict Survival"):
    user_data = {
        "Pclass": pclass, "Sex": sex, "Age": age, "FamilySize": family_size, "Fare": fare,
        "Embarked_C": embarked_C, "Embarked_Q": embarked_Q, "Embarked_S": embarked_S
    }

    try:
        response = requests.post("http://127.0.0.1:5000/predict", json=user_data)
        result = response.json()

        if "error" in result:
            st.error("Error: " + result["error"])
        else:
            outcome = "🟢 Survived" if result["survived"] == 1 else "🔴 Not Survived"
            probability = result["probability"]

            # 🔹 Stylish Prediction Result
            st.markdown(
                f"""
                <div style="text-align: center; padding: 20px; border-radius: 15px;
                            background-color: rgba(255,255,255,0.8); box-shadow: 0px 4px 8px rgba(0,0,0,0.2);">
                    <h2 style="color: #333;">Result: {outcome}</h2>
                    <p style="font-size: 18px;">Confidence Level: {probability:.2f}%</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error("Failed to connect to the prediction server. Is it running?")
