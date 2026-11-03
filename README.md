## Introduction

Weather Data Analyzer is a menu-driven Python program that reads daily weather observations from a CSV file. It can report summary statistics, clean incomplete or duplicate records, save a cleaned CSV file, and display temperature and rainfall charts.

## Objectives

- Analyze weather readings stored in a CSV file.
- Calculate useful temperature and rainfall statistics.
- Identify and remove duplicate or incomplete records.
- Present weather trends with charts.

## Features

- **Summary:** Shows average temperature, maximum and minimum temperatures with dates, temperature standard deviation, and total rainfall.
- **Clean & Plot:** Removes duplicate rows and rows with missing or invalid required values, saves the remaining records to `cleaned_weather_data.csv`, and displays a temperature line chart and rainfall bar chart.
- **Input validation:** Checks for the expected CSV columns and reports missing or unreadable input files in a clear way.
- **Menu:** Offers Summary, Clean & Plot, and Exit options.

## Requirements

- Python 3.14
- pandas
- numpy
- matplotlib

## Installation

1. Install Python 3.14 if it is not already installed.
2. Open a terminal or command prompt in the folder containing the project files.
3. Install the required libraries:

   ```bash
   python -m pip install pandas numpy matplotlib
   ```

## Project files

- `one.py` — complete Python program.
- `weather_data.csv` — sample input data.
- `cleaned_weather_data.csv` — generated when the Clean & Plot option runs successfully.

Keep `one.py` and `weather_data.csv` in the same folder. The CSV must contain these column names: `Date`, `Temp`, `Humidity`, and `Rainfall`.

## How to run

From the project folder, run:

```bash
python one.py
```

At the menu, enter `1` for Summary, `2` for Clean & Plot, or `3` to Exit. You can also type the option names shown by the program. Close the chart window to return to the menu.

## Input and output

**Input:** `weather_data.csv`, with one weather observation per row. Dates should be parseable as dates, and the other three columns should contain numeric values. Invalid or missing values are excluded during cleaning. If the input file is missing or does not have the required columns, the program prints an explanation and exits gracefully.

**Outputs:** Summary statistics are printed in the terminal. Clean & Plot writes `cleaned_weather_data.csv` in the same folder as the script and displays two charts: temperature over time and rainfall by date.

## Notes

The standard deviation is calculated from the sample when at least two valid temperature readings are available. When only one reading is available, the program reports that standard deviation is unavailable.
