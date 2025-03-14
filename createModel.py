import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import h2o
from h2o.automl import H2OAutoML

# Initialize H2O
h2o.init()

# Load your CSV dataset (make sure your CSV has two columns: "state" and "action")
df = pd.read_csv("data.csv")
print("Original Data:")
print(df.head())

# Use TF-IDF to transform the 'state' text into numeric features
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["state"]).toarray()

import joblib
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

# Create a DataFrame from the TF-IDF features
feature_names = vectorizer.get_feature_names_out()
df_features = pd.DataFrame(tfidf_matrix, columns=feature_names)

# Combine the features with the target label
df_combined = pd.concat([df_features, df["action"]], axis=1)

# Convert the Pandas DataFrame to an H2OFrame
hf = h2o.H2OFrame(df_combined)

# Specify the response (target) column and predictor columns
response = "action"
predictors = [col for col in hf.columns if col != response]

# Convert the target column to a factor (categorical variable)
hf[response] = hf[response].asfactor()

# Run H2O AutoML (here we limit runtime to 5 minutes for demonstration)
aml = H2OAutoML(max_runtime_secs=600, seed=1)
aml.train(x=predictors, y=response, training_frame=hf)

# View the leaderboard of models
lb = aml.leaderboard
print("Leaderboard:")
print(lb)

#store the model to disk
model_path = h2o.save_model(model=aml.leader, path=".", force=True)
print(model_path)

# Shutdown H2O
h2o.cluster().shutdown()
# The model is saved to disk and can be loaded for making predictions on new data.
# The vectorizer used for transforming the text data to TF-IDF features is also saved for consistency.
# The model can be loaded in a separate script for making predictions on new data.
# The vectorizer can be loaded to transform the new data in the same way as the training data.
# The new data can then be used to make predictions using the loaded model.
# The model can be used to predict the target label for new data based on the TF-IDF features of the text data.