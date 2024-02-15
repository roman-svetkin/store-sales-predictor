# Store Sales Prediction App

## Overview

This Store Sales Prediction App is designed to help predict stores sales based on its area characteristics. It utilises a trained model to offer predictions directly within a web interface.

## Features

- Predict Store Sales using store area characteristics.
- Upload store data in CSV format for predictions.
- Download the predictions appended to the uploaded data.

## How to Use

1. Navigate to the Streamlit app URL - <https://store-sales-predictor.streamlit.app/>
2. Upload your data as a CSV file by clicking on the "Upload your input CSV file" button.
3. The app will display a preview of the uploaded file.
4. Click on "Predict" to generate store sales predictions, which will be added to the DataFrame and displayed.
5. Download the DataFrame with predictions by clicking on the provided link.

## Model Information

The prediction model is an Random Forest model trained on stores data, saved as `best_rf_model.joblib`. It predicts store sales based on store area characteristics.

## Prediction and Download

After processing the uploaded data, predictions are made and appended to the uploaded DataFrame. Users can download the result as a CSV file.

## Developer Notes

- Adjust the path to the model file as needed.
- Customise categorical and numerical features based on your model's training.

## Quick Start on Local

Clone the app's repository, install the dependencies (Python 3.11.7), and run the Streamlit app using `streamlit run app.py --server.enableXsrfProtection=false --server.port=7860`.

---
