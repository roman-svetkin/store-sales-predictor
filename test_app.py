import numpy as np
import pandas as pd

from app import KNNImputer, download_link, most_important_features, predict, scaler

pd.options.mode.copy_on_write = True

# Load the test data
input_df = pd.read_csv("test.csv")

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


def test_predict():
    """
    A function that takes a pandas DataFrame as input and returns a pandas Series. It calls the predict function and then performs checks on the returned predictions.
    """

    # Call the predict function
    predictions = predict(X_test_scaled_df)

    # Check if predictions are returned as expected
    assert isinstance(
        predictions, np.ndarray
    ), "Predictions should be returned as an array"
    assert len(predictions) > 0, "Should return a non-empty series of predictions"
    assert int(predictions[11]) == 2


preds = predict(X_test_scaled_df)

# Append predictions to the DataFrame
input_df["Predicted Interest Rate"] = preds


def test_download_link() -> None:
    """
    Call the download_link function
    Check if the link is correctly formatted
    """
    # Call the download_link function
    link = download_link(input_df, "predictions.csv", "Download Predictions")

    # Check if the link is correctly formatted
    assert "predictions.csv" in link, "The download link should be correctly formatted"
