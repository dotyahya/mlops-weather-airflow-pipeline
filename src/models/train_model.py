import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

import pickle
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import os

def train_model():
    df = pd.read_csv("data/processed_data.csv")

    # define features and target
    X = df[['humidity', 'wind_speed']]
    y = df['temperature']

    # split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # make predictions
    y_pred = model.predict(X_test)
    
    # define metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    # initialie mlflow
    mlflow.set_experiment("weather_temperature_prediction")

    with mlflow.start_run():
        # log metrics
        mlflow.log_metrics({
            "mse": mse,
            "r2": r2,
            "mae": mae
        })

        # tagging
        mlflow.set_tag("Training Info", "Linear Regression model for temperature prediction")
        mlflow.set_tag("Features", "humidity, wind_speed")
        mlflow.set_tag("Target", "temperature")

        signature = infer_signature(X_train, model.predict(X_train))

        # log model
        try:
            model_info = mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="temperature_model",
                signature=signature,
                input_example=X_train,
                registered_model_name="weather-temperature-predictor"
            )
            
            loaded_model = mlflow.pyfunc.load_model(model_info.model_uri)

            results = pd.DataFrame({
                'humidity': X_test['humidity'],
                'wind_speed': X_test['wind_speed'],
                'actual_temperature': y_test,
                'predicted_temperature': loaded_model.predict(X_test)
            })
            
            print("\nModel Performance Metrics:")
            print(f"MSE: {mse:.2f}")
            print(f"R2 Score: {r2:.2f}")
            print(f"MAE: {mae:.2f}")
            
            print("\nSample Predictions:")
            print(results.head())
            
        except Exception as e:
            print(f"Error registering model: {e}")

    os.makedirs("models", exist_ok=True)
    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)

if __name__ == "__main__":
    train_model()










