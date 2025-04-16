# --- 1. Import Libraries ---
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib # For saving the model

print("Libraries imported successfully.")

# --- 2. Load Data ---
# Load the Titanic dataset from a CSV file
try:
    df = pd.read_csv(r'train.csv')
    print("Dataset loaded successfully.")
    print("Dataset shape:", df.shape)
    print(df.head()) # Optional: uncomment to see the first few rows
except FileNotFoundError:
    print("Error: train.csv not found. Make sure it's in the same directory.")
    exit() 

# --- 3. Define Features (X) and Target (y) ---
# Select features that seem relevant and are easier to handle initially
# drop PassengerId, Name, Ticket, Cabin for simplicity
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
target = 'Survived'

X = df[features]
y = df[target]

print(f"Features selected: {features}")
print(f"Target variable: {target}")

# --- 4. Preprocessing Steps ---
# Define preprocessing for numerical features (impute missing values, then scale)
# impute 'Age' and 'Fare' with the median
numerical_features = ['Age', 'Fare', 'SibSp', 'Parch']
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')), # Handle missing numerical values
    ('scaler', StandardScaler()) # Scale numerical features
])

# Define preprocessing for categorical features (impute missing values, then one-hot encode)
# impute 'Embarked' with the most frequent value
categorical_features = ['Sex', 'Embarked', 'Pclass'] # Pclass is categorical in nature
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')), # Handle missing categorical values
    ('onehot', OneHotEncoder(handle_unknown='ignore')) # Convert categories to numbers
])

# Create a preprocessor object using ColumnTransformer
# applies different transformers to different columns
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='passthrough' # Keep other columns (if any), though we selected all needed
)

print("Preprocessing pipeline created.")

# --- 5. Split Data into Training and Testing Sets ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Data split into training ({X_train.shape[0]} samples) and testing ({X_test.shape[0]} samples).")

# --- 6. Create and Train the Logistic Regression Model ---
# combine the preprocessor and the model into a single pipeline
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(solver='liblinear', random_state=42))])

print("Training the Logistic Regression model...")
model_pipeline.fit(X_train, y_train)
print("Model training completed.")

# --- 7. Evaluate the Model ---
print("\n--- Model Evaluation ---")
y_pred = model_pipeline.predict(X_test)
print(f"Predictions made for {len(y_pred)} samples.")
print(f"First 5 predictions: {y_pred[:5]}")

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# --- 8. Save the Trained Model Pipeline ---
model_filename = 'titanic_logistic_regression_model.joblib'
joblib.dump(model_pipeline, model_filename)
print(f"\nModel pipeline saved successfully as '{model_filename}'.")