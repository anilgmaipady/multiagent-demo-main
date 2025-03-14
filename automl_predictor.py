# automl_predictor.py
import h2o
import pandas as pd
import joblib

import h2o
from h2o.automl import H2OAutoML
import pandas as pd

# Initialize H2O (if not already running)
if not h2o.connection():
    h2o.init()

# Define the paths to your saved model and vectorizer.
# Update these paths as needed.
MODEL_PATH = "./StackedEnsemble_BestOfFamily_1_AutoML_1_20250304_123221"
VECTORIZER_PATH = "tfidf_vectorizer.pkl"

# Load the H2O model and the TF-IDF vectorizer
aml_model = h2o.load_model(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def predict_action(state: dict) -> str:
    """
    Given a state dictionary, convert it to a text string,
    transform it using the saved TF-IDF vectorizer,
    and predict the supply chain action using the H2O AutoML model.
    
    Expected state format (keys should match training):
    {
      "supplier_inventory": 100,
      "manufacturer_capacity": 50,
      "manufacturer_inventory": 0,
      "distributor_inventory": 50,
      "retail_inventory": 10,
      "retailer_customer_demand": 40,
      "backorders": 5,
      "forecast_demand": 45
    }
    """
    # Convert the state dict to a string in the same format as in training.
    state_str = ", ".join(f"{key}={value}" for key, value in state.items())
    
    # Transform the state string to TF-IDF features
    tfidf_matrix = vectorizer.transform([state_str]).toarray()
    feature_names = vectorizer.get_feature_names_out()
    df_features = pd.DataFrame(tfidf_matrix, columns=feature_names)
    
    # Convert the DataFrame to an H2OFrame
    hf = h2o.H2OFrame(df_features)
    
    # Predict using the leader model
    predictions = aml_model.predict(hf)
    
    # The predictions H2OFrame usually has the predicted label in the first column
    predicted_action = predictions[0, 0]
    return predicted_action
