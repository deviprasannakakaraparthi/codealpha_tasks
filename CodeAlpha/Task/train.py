import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load Dataset
data = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
data.drop(["Name", "Ticket", "Cabin"], axis=1, inplace=True)

# Feature Engineering
data["FamilySize"] = data["SibSp"] + data["Parch"]
data.drop(["SibSp", "Parch"], axis=1, inplace=True)

# Handle Missing Values
data["Age"].fillna(data["Age"].median(), inplace=True)
data["Embarked"].fillna(data["Embarked"].mode()[0], inplace=True)

# Convert Categorical Variables
data["Sex"] = LabelEncoder().fit_transform(data["Sex"])
data = pd.get_dummies(data, columns=["Embarked"], drop_first=True)

# Define Features and Target Variables
X = data.drop("Survived", axis=1)
y = data["Survived"]

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale Features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train Model
param_grid = {"n_estimators": [50, 100, 200], "max_depth": [None, 5, 10]}
gs = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring="accuracy")
gs.fit(X_train, y_train)
best_model = gs.best_estimator_

# Save Model & Scaler
with open("titanic_model.pkl", "wb") as model_file:
    pickle.dump(best_model, model_file)

with open("scaler.pkl", "wb") as scaler_file:
    pickle.dump(scaler, scaler_file)

print("✅ Model and Scaler Saved Successfully!")
