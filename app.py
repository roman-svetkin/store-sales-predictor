import base64

import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.impute import KNNImputer

pd.options.mode.copy_on_write = True

# Load the saved model and scaler
model_path = "./model/best_rf_model.joblib"
scaler_path = "./model/std_scaler.bin"

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# Define the columns to keep
most_important_features = [
    "crime_rate",
    "proportion_flats",
    "proportion_nonretail",
    "commercial_property",
    "household_size",
    "proportion_newbuilds",
    "public_transport_dist",
    "property_value",
    "school_proximity",
    "competitor_density",
    "household_affluency",
]


def download_link(
    object_to_download: pd.DataFrame, download_filename: str, download_link_text: str
) -> str:
    """
    Generates a link to download the given object_to_download.
    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(
            index=False
        )  # Convert DataFrame to CSV
    b64 = base64.b64encode(
        object_to_download.encode()
    ).decode()  # Encode CSV data to base64
    return f'<a href="data:file/csv;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


def predict(input_data: np.ndarray) -> np.ndarray:
    """
    Make a prediction using the trained model.

    Note: input_data is expected to be a NumPy array after preprocessing.
    """
    # Assuming input_data is already prepared as a NumPy array for prediction
    prediction = model.predict(input_data)
    return prediction


st.title("Store Sales Predictor App")

st.markdown(
    """
This app allows you to predict stores sales based on the features of the store's location.
Please upload your data as a CSV file. Ensure your data includes the necessary features that the model expects.
"""
)

# Create a file uploader for the user to upload files
uploaded_file = st.file_uploader("Upload your input CSV file", type="csv")

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)

    # Display the uploaded file
    st.write("Preview of uploaded file:")
    st.write(input_df.head())

    # Select the most important features
    X_test_new = input_df[most_important_features]

    # Impute missing values
    imputer = KNNImputer(n_neighbors=5)
    df_imputed = imputer.fit_transform(X_test_new)
    X_test_new = pd.DataFrame(df_imputed, columns=X_test_new.columns)

    numerical_columns = list(X_test_new.select_dtypes(include=[np.number]).columns)

    # Scale the data
    X_test_scaled = scaler.transform(X_test_new)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=numerical_columns)

    if st.button("Predict"):

        preds = predict(X_test_scaled_df)

        # Append predictions to the DataFrame
        input_df["Predicted Store Sales"] = preds

        st.write("Predictions have been added to the DataFrame:")
        st.write(input_df.head())

        # Generate a link for downloading the results
        tmp_download_link = download_link(
            input_df, "predictions.csv", "Click here to download your predictions!"
        )
        st.markdown(tmp_download_link, unsafe_allow_html=True)

else:
    st.write("Please upload a file to begin.")
