import pandas as pd


DATASET_PATH = (
    "Mumbai_1990_2022_Santacruz.csv"
)


def prepare_dataset():
    df = pd.read_csv(DATASET_PATH)

    df["time"] = pd.to_datetime(
        df["time"],
        dayfirst=True
    )

    df = df.sort_values("time")

    # Keep rows with actual rainfall observations.
    df = df.dropna(subset=["prcp"]).copy()

    # Calendar features
    df["month"] = df["time"].dt.month
    df["day_of_year"] = df["time"].dt.dayofyear

    # Previous rainfall
    df["rainfall_previous_day"] = (
        df["prcp"].shift(1)
    )

    # Rolling rainfall history
    df["rainfall_3day"] = (
        df["prcp"]
        .shift(1)
        .rolling(3)
        .sum()
    )

    df["rainfall_7day"] = (
        df["prcp"]
        .shift(1)
        .rolling(7)
        .sum()
    )

    # Heavy-rainfall target
    df["heavy_rain"] = (
        df["prcp"] >= 50
    ).astype(int)

    # Remove rows that don't have enough history
    df = df.dropna(
        subset=[
            "rainfall_previous_day",
            "rainfall_3day",
            "rainfall_7day"
        ]
    )

    return df
if __name__ == "__main__":
    df = prepare_dataset()

    print("Training records:", len(df))
    print(
        "Heavy-rainfall records:",
        df["heavy_rain"].sum()
    )
    print(
        "Normal-rainfall records:",
        (df["heavy_rain"] == 0).sum()
    )

    print("\nFeatures:")
    print(df[
        [
            "time",
            "prcp",
            "month",
            "day_of_year",
            "rainfall_previous_day",
            "rainfall_3day",
            "rainfall_7day",
            "heavy_rain"
        ]
    ].head(10))