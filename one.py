"""Weather Data Analyzer

Analyze a CSV file containing Date, Temp, Humidity, and Rainfall columns.
Requires Python 3.14, pandas, numpy, and matplotlib.
"""

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


REQUIRED_COLUMNS = ["Date", "Temp", "Humidity", "Rainfall"]
INPUT_FILE = Path(__file__).resolve().with_name("weather_data.csv")
OUTPUT_FILE = Path(__file__).resolve().with_name("cleaned_weather_data.csv")


def load_data(file_path: Path = INPUT_FILE) -> pd.DataFrame | None:
    """Read and validate the weather CSV; return None on a recoverable error."""
    if not file_path.is_file():
        print(f"CSV file not found: {file_path.name}")
        print("Place weather_data.csv in the same folder as this program.")
        return None
    try:
        data = pd.read_csv(file_path)
    except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError) as exc:
        print(f"Could not read {file_path.name}: {exc}")
        return None

    missing = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing:
        print("CSV is missing required column(s): " + ", ".join(missing))
        print("Required columns: " + ", ".join(REQUIRED_COLUMNS))
        return None

    data = data[REQUIRED_COLUMNS].copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    for column in ("Temp", "Humidity", "Rainfall"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    return data


def summarize(data: pd.DataFrame) -> None:
    """Print descriptive statistics using available, valid observations."""
    valid = data.dropna(subset=["Date", "Temp"])
    print("\nWeather Summary")
    print("---------------")
    if valid.empty:
        print("No valid temperature/date records are available.")
    else:
        temps = valid["Temp"]
        average = float(np.mean(temps.to_numpy()))
        max_index, min_index = temps.idxmax(), temps.idxmin()
        print(f"Average temperature: {average:.2f}")
        print(f"Maximum temperature: {data.at[max_index, 'Temp']:g} on {data.at[max_index, 'Date'].date()}")
        print(f"Minimum temperature: {data.at[min_index, 'Temp']:g} on {data.at[min_index, 'Date'].date()}")
        print(f"Temperature standard deviation: {float(np.std(temps.to_numpy(), ddof=1)):.2f}" if len(temps) > 1 else "Temperature standard deviation: not available (one observation)")

    rainfall = data["Rainfall"].dropna()
    if rainfall.empty:
        print("Total rainfall: not available (no valid rainfall values)")
    else:
        print(f"Total rainfall: {float(np.sum(rainfall.to_numpy())):.2f}")
    print()


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate rows and records missing required values."""
    before = len(data)
    cleaned = data.drop_duplicates().dropna(subset=REQUIRED_COLUMNS).copy()
    print(f"Removed {before - len(data.drop_duplicates())} duplicate row(s).")
    print(f"Removed {len(data.drop_duplicates()) - len(cleaned)} row(s) with missing or invalid values.")
    return cleaned.sort_values("Date").reset_index(drop=True)


def plot_data(data: pd.DataFrame) -> None:
    """Display a temperature line chart and a rainfall bar chart."""
    if data.empty:
        print("No complete records are available to plot.")
        return
    fig, (temperature_ax, rainfall_ax) = plt.subplots(2, 1, figsize=(10, 8), constrained_layout=True)
    temperature_ax.plot(data["Date"], data["Temp"], marker="o", color="tab:red")
    temperature_ax.set(title="Temperature Over Time", xlabel="Date", ylabel="Temperature")
    temperature_ax.grid(True, alpha=0.3)

    rainfall_ax.bar(data["Date"].dt.strftime("%Y-%m-%d"), data["Rainfall"], color="tab:blue")
    rainfall_ax.set(title="Rainfall by Date", xlabel="Date", ylabel="Rainfall")
    rainfall_ax.tick_params(axis="x", rotation=45)
    rainfall_ax.grid(axis="y", alpha=0.3)
    plt.show()


def clean_and_plot(data: pd.DataFrame) -> None:
    cleaned = clean_data(data)
    try:
        cleaned.to_csv(OUTPUT_FILE, index=False, date_format="%Y-%m-%d")
    except OSError as exc:
        print(f"Could not save cleaned CSV: {exc}")
    else:
        print(f"Cleaned data saved to: {OUTPUT_FILE.name}")
    plot_data(cleaned)


def main() -> int:
    data = load_data()
    if data is None:
        return 0

    while True:
        print("Weather Data Analyzer")
        print("1. Summary")
        print("2. Clean & Plot")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()
        if choice in {"1", "summary"}:
            summarize(data)
        elif choice in {"2", "clean & plot", "clean and plot"}:
            clean_and_plot(data)
        elif choice in {"3", "exit"}:
            print("Goodbye!")
            return 0
        else:
            print("Invalid choice. Enter 1, 2, or 3.\n")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (EOFError, KeyboardInterrupt):
        print("\nProgram ended.")
        raise SystemExit(0)
