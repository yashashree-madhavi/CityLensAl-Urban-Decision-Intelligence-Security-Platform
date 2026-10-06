import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

from app.ai.prepare_dataset import prepare_dataset


FEATURES = [
    "month",
    "day_of_year",
    "rainfall_previous_day",
    "rainfall_3day",
    "rainfall_7day"
]

TARGET = "heavy_rain"

MODEL_PATH = "app/ai/flood_model.joblib"


def train_model():

    df = prepare_dataset()

    X = df[FEATURES]
    y = df[TARGET]

    # Chronological split
    split_index = int(len(df) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\nModel Evaluation:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=[
                "Normal Rain",
                "Heavy Rain"
            ],
            zero_division=0
        )
    )

    joblib.dump(model, MODEL_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_model()