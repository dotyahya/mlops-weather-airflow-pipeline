import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

def preprocess_data():
    df = pd.read_csv("data/raw_data.csv")
    
    df = df.fillna(df.mean(numeric_only=True))
    scaler = StandardScaler()
    numerical_cols = ["temperature", "humidity", "wind_speed"]
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    # save processed data into data/ dir along with raw_data.csv
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/processed_data.csv", index=False)

if __name__ == "__main__":
    preprocess_data()