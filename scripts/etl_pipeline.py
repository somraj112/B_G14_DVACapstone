"""ETL pipeline for NST DVA Capstone 2 — US Accidents analysis.

Problem framing:
    Identifying high-risk road conditions and geographic hotspots to reduce
    traffic accident severity across the United States.

This module exposes both the original generic helpers (normalize_columns,
basic_clean, save_processed) and a full US-Accidents cleaning pipeline used by
notebooks 02 and 05.

CLI:
    python scripts/etl_pipeline.py \
        --input data/raw/US_Accidents_March23.csv \
        --output data/processed/cleaned_dataset.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Generic helpers (kept for reuse)
# ---------------------------------------------------------------------------

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names to a clean snake_case format."""
    cleaned = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    result = df.copy()
    result.columns = cleaned
    return result


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply safe default cleaning: normalize columns, drop duplicates, trim strings."""
    result = normalize_columns(df)
    result = result.drop_duplicates().reset_index(drop=True)
    for column in result.select_dtypes(include="object").columns:
        result[column] = result[column].astype("string").str.strip()
    return result


def save_processed(df: pd.DataFrame, output_path: Path) -> None:
    """Write dataframe to disk, creating parent folders as needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


# ---------------------------------------------------------------------------
# US Accidents — column groups
# ---------------------------------------------------------------------------

# Columns dropped because they are redundant, free-text, constant, or not useful
# for a government-facing severity analysis.
DROP_COLUMNS: tuple[str, ...] = (
    "id",
    "source",
    "description",
    "end_lat",
    "end_lng",
    "number",
    "airport_code",
    "weather_timestamp",
    "country",
    "turning_loop",
    "nautical_twilight",
    "astronomical_twilight",
)

NUMERIC_WEATHER_COLUMNS: tuple[str, ...] = (
    "temperature_f",
    "wind_chill_f",
    "humidity",
    "pressure_in",
    "visibility_mi",
    "wind_speed_mph",
    "precipitation_in",
)

CATEGORICAL_FILL_COLUMNS: tuple[str, ...] = (
    "wind_direction",
    "weather_condition",
    "zipcode",
    "city",
    "county",
    "street",
    "timezone",
    "sunrise_sunset",
    "civil_twilight",
)

BOOLEAN_POI_COLUMNS: tuple[str, ...] = (
    "amenity",
    "bump",
    "crossing",
    "give_way",
    "junction",
    "no_exit",
    "railway",
    "roundabout",
    "station",
    "stop",
    "traffic_calming",
    "traffic_signal",
)

SEVERITY_LABELS: dict[int, str] = {
    1: "Low",
    2: "Moderate",
    3: "High",
    4: "Critical",
}


# ---------------------------------------------------------------------------
# US Accidents — loading
# ---------------------------------------------------------------------------

def load_us_accidents(
    input_path: Path | str,
    sample_n: int | None = None,
    random_state: int = 42,
) -> pd.DataFrame:
    """Load the raw US Accidents CSV and normalize column names.

    Parameters
    ----------
    input_path : path to the combined raw CSV (produced by data/raw/combine.py)
    sample_n   : if given, return a random sample of this many rows (for dev)
    random_state : seed for reproducible sampling
    """
    input_path = Path(input_path)
    df = pd.read_csv(input_path, low_memory=False)
    df = normalize_columns(df)

    if sample_n is not None and sample_n < len(df):
        df = df.sample(n=sample_n, random_state=random_state).reset_index(drop=True)

    return df


# ---------------------------------------------------------------------------
# US Accidents — cleaning stages
# ---------------------------------------------------------------------------

def drop_unused_columns(df: pd.DataFrame, columns: Iterable[str] = DROP_COLUMNS) -> pd.DataFrame:
    """Drop columns that are not used in the government-facing severity analysis."""
    to_drop = [c for c in columns if c in df.columns]
    return df.drop(columns=to_drop)


def parse_datetimes(df: pd.DataFrame) -> pd.DataFrame:
    """Parse Start_Time and End_Time as datetime."""
    result = df.copy()
    for col in ("start_time", "end_time"):
        if col in result.columns:
            result[col] = pd.to_datetime(result[col], errors="coerce")
    return result


def drop_missing_critical(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows missing fields that are required for downstream analysis."""
    required = [c for c in ("severity", "start_time", "state", "start_lat", "start_lng")
                if c in df.columns]
    return df.dropna(subset=required).reset_index(drop=True)


def impute_weather(df: pd.DataFrame) -> pd.DataFrame:
    """Median-impute numeric weather columns (robust to skew)."""
    result = df.copy()
    for col in NUMERIC_WEATHER_COLUMNS:
        if col in result.columns:
            result[col] = pd.to_numeric(result[col], errors="coerce")
            median = result[col].median()
            result[col] = result[col].fillna(median)
    return result


def impute_categorical(df: pd.DataFrame) -> pd.DataFrame:
    """Fill categorical columns with 'Unknown' so rows are preserved."""
    result = df.copy()
    for col in CATEGORICAL_FILL_COLUMNS:
        if col in result.columns:
            result[col] = result[col].astype("object").fillna("Unknown")
    return result


def coerce_booleans(df: pd.DataFrame) -> pd.DataFrame:
    """Force POI columns to boolean dtype."""
    result = df.copy()
    for col in BOOLEAN_POI_COLUMNS:
        if col in result.columns:
            result[col] = result[col].fillna(False).astype(bool)
    return result


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derive hour / day / month / year / season / rush-hour / weekend flags."""
    result = df.copy()
    if "start_time" not in result.columns:
        return result

    st = result["start_time"]
    result["hour"] = st.dt.hour
    result["day_of_week"] = st.dt.dayofweek  # Monday=0
    result["day_name"] = st.dt.day_name()
    result["month"] = st.dt.month
    result["month_name"] = st.dt.month_name()
    result["year"] = st.dt.year
    result["date"] = st.dt.date

    season_map = {
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Fall", 10: "Fall", 11: "Fall",
    }
    result["season"] = result["month"].map(season_map)

    result["is_weekend"] = result["day_of_week"] >= 5
    result["is_rush_hour"] = result["hour"].between(7, 9) | result["hour"].between(16, 19)

    return result


def add_duration(df: pd.DataFrame, max_minutes: int = 24 * 60) -> pd.DataFrame:
    """Compute accident duration in minutes and drop implausible values."""
    result = df.copy()
    if not {"start_time", "end_time"}.issubset(result.columns):
        return result

    delta = (result["end_time"] - result["start_time"]).dt.total_seconds() / 60.0
    result["duration_min"] = delta

    # Drop negative durations or those longer than a day (data errors).
    mask = result["duration_min"].between(0, max_minutes)
    result = result.loc[mask].reset_index(drop=True)
    return result


def add_severity_label(df: pd.DataFrame) -> pd.DataFrame:
    """Map numeric Severity (1-4) to human-readable labels + binary high-severity flag."""
    result = df.copy()
    if "severity" not in result.columns:
        return result
    result["severity"] = pd.to_numeric(result["severity"], errors="coerce").astype("Int64")
    result["severity_label"] = result["severity"].map(SEVERITY_LABELS)
    result["is_high_severity"] = result["severity"] >= 3
    return result


def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Cap distance at 99th percentile and remove impossible temperatures."""
    result = df.copy()
    if "distance_mi" in result.columns:
        result["distance_mi"] = pd.to_numeric(result["distance_mi"], errors="coerce")
        cap = result["distance_mi"].quantile(0.99)
        result["distance_mi"] = result["distance_mi"].clip(upper=cap)
    if "temperature_f" in result.columns:
        result = result[result["temperature_f"].between(-60, 140)].reset_index(drop=True)
    return result


# ---------------------------------------------------------------------------
# US Accidents — orchestrator
# ---------------------------------------------------------------------------

def clean_us_accidents(df: pd.DataFrame) -> pd.DataFrame:
    """Full cleaning pipeline for the US Accidents dataset."""
    df = normalize_columns(df)
    df = drop_unused_columns(df)
    df = parse_datetimes(df)
    df = drop_missing_critical(df)
    df = impute_weather(df)
    df = impute_categorical(df)
    df = coerce_booleans(df)
    df = add_duration(df)
    df = add_time_features(df)
    df = add_severity_label(df)
    df = handle_outliers(df)
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def build_clean_dataset(input_path: Path | str, sample_n: int | None = None) -> pd.DataFrame:
    """Load raw CSV, apply the US Accidents pipeline, return cleaned dataframe."""
    raw = load_us_accidents(input_path, sample_n=sample_n)
    return clean_us_accidents(raw)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Capstone 2 US Accidents ETL pipeline.")
    parser.add_argument("--input", required=True, type=Path, help="Raw CSV in data/raw/.")
    parser.add_argument("--output", required=True, type=Path, help="Cleaned CSV in data/processed/.")
    parser.add_argument("--sample", type=int, default=None, help="Optional dev sample size.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cleaned = build_clean_dataset(args.input, sample_n=args.sample)
    save_processed(cleaned, args.output)
    print(f"Processed dataset saved to: {args.output}")
    print(f"Rows: {len(cleaned):,} | Columns: {len(cleaned.columns)}")


if __name__ == "__main__":
    main()
