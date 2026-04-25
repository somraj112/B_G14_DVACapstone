# Data Dictionary — US Accidents (2016–2023)

## Dataset Summary

| Item | Details |
|---|---|
| Dataset name | US Accidents (Feb 2016 – Mar 2023) |
| Source | Moosavi, S. et al. — Kaggle (sobhanmoosavi/us-accidents) |
| Raw file name | `US_Accidents_March23.csv` (produced locally by `data/raw/combine.py`) |
| Last updated | March 2023 |
| Granularity | one row per traffic accident record across 49 US states |
| Row count | ~7.7 million |
| Column count (raw) | 46 |
| Column count (cleaned) | ~34 (after drops + derived features) |

## Column Definitions — Raw Columns Retained After Cleaning

| Column Name | Data Type | Description | Example | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `severity` | int (1–4) | Traffic impact severity: 1 = low, 4 = critical | 2 | EDA, stats, all KPIs, dashboard | Target variable — rows with nulls dropped |
| `start_time` | datetime | Accident start timestamp | 2020-05-17 07:13:00 | Time features, trends | Parsed to datetime, rows with nulls dropped |
| `end_time` | datetime | Accident end timestamp | 2020-05-17 08:02:00 | Duration calc | Parsed to datetime, used only to derive `duration_min` |
| `start_lat`, `start_lng` | float | Accident latitude / longitude | 33.77, -84.38 | Map view in Tableau | Rows with null coordinates dropped |
| `distance_mi` | float | Length of road segment affected | 0.45 | EDA, stats | Capped at 99th percentile |
| `street` | string | Street / road name | I-85 N | Drill-down | Filled `Unknown` |
| `city`, `county`, `state`, `zipcode` | string | Administrative geography | Atlanta, Fulton, GA, 30301 | Hotspot KPIs | `Unknown` fill for city / county / zip; state non-null |
| `timezone` | string | IANA timezone of accident | US/Eastern | Optional filter | `Unknown` fill |
| `temperature_f` | float | Air temperature at event | 72.0 | Weather analysis | Median imputed; removed if < -60 or > 140 |
| `wind_chill_f` | float | Wind chill | 70.0 | Weather analysis | Median imputed |
| `humidity` | float (%) | Relative humidity | 58.0 | Weather analysis | Median imputed |
| `pressure_in` | float (in Hg) | Atmospheric pressure | 30.01 | Weather analysis | Median imputed |
| `visibility_mi` | float | Visibility | 10.0 | Weather analysis, stats | Median imputed |
| `wind_direction` | string | Wind direction | NW | Weather analysis | `Unknown` fill |
| `wind_speed_mph` | float | Wind speed | 5.8 | Weather analysis | Median imputed |
| `precipitation_in` | float | Precipitation | 0.0 | Weather analysis | Median imputed |
| `weather_condition` | string | Text weather label | Light Rain | Weather KPI, chi-square | `Unknown` fill |
| `amenity`, `bump`, `crossing`, `give_way`, `junction`, `no_exit`, `railway`, `roundabout`, `station`, `stop`, `traffic_calming`, `traffic_signal` | bool | Point-of-interest flags within ~150 m of the accident | True | Infrastructure KPIs, stats | Forced to bool; `False` default |
| `sunrise_sunset` | string | `Day` / `Night` at accident start | Day | Day-night KPI, stats | `Unknown` fill |
| `civil_twilight` | string | Civil twilight flag | Day | Optional filter | `Unknown` fill |

## Columns Dropped in Cleaning

| Column | Reason |
|---|---|
| `id` | internal identifier, not analytical |
| `source` | API provider, not analytical |
| `description` | free text, not structured for this analysis |
| `end_lat`, `end_lng` | ~50% null, redundant with `start_lat` / `start_lng` |
| `number` | street number, ~60% null |
| `airport_code` | audit field for the weather join |
| `weather_timestamp` | audit field |
| `country` | constant = `US` |
| `turning_loop` | constant = `False` |
| `nautical_twilight`, `astronomical_twilight` | redundant with `sunrise_sunset` / `civil_twilight` |

## Derived Columns (added in cleaning)

| Derived Column | Logic | Business Meaning |
|---|---|---|
| `duration_min` | `(end_time − start_time)` in minutes | Time traffic was blocked — emergency response metric |
| `hour` | `start_time.hour` | Enables rush-hour analysis |
| `day_of_week` | 0 = Monday … 6 = Sunday | Weekday vs weekend patterns |
| `day_name` | Monday / Tuesday / … | Human-readable for dashboard |
| `month`, `month_name` | 1–12 / January–December | Seasonality |
| `year` | `start_time.year` | YoY trend, growth KPI |
| `date` | `start_time.date()` | Daily aggregations |
| `season` | Winter (Dec–Feb), Spring (Mar–May), Summer (Jun–Aug), Fall (Sep–Nov) | Seasonal budgeting decisions |
| `is_weekend` | `day_of_week >= 5` | Weekend-vs-weekday comparisons |
| `is_rush_hour` | hour ∈ [7,9] ∪ [16,19] | Peak-hour staffing |
| `severity_label` | 1 → Low, 2 → Moderate, 3 → High, 4 → Critical | Human-readable severity |
| `is_high_severity` | `severity ≥ 3` | Binary target for logistic regression |

## Data Quality Notes

- **Coverage gap:** the dataset has uneven collection across states — California, Florida, and Texas are over-represented relative to population. Conclusions about absolute volume should be interpreted accordingly; severity *rates* (per-accident) are more comparable across states.
- **Source API changes:** historical weather values are joined from airport weather stations and may be up to a few miles from the accident location.
- **Duration extremes:** negative durations and values above 24 hours were removed as data-entry errors.
- **Distance extremes:** `distance_mi` has a heavy right tail; capped at the 99th percentile.
- **Temperature sanity:** readings outside [−60 °F, 140 °F] were removed.
- **Post-2020 volume spike:** a jump in 2021 likely reflects expanded API coverage, not a real accident surge; this is documented as a caveat in the final report.
- **No population normalisation:** the dataset does not include population or VMT (vehicle-miles-travelled) to normalise rates. Recommendations therefore focus on within-dataset rates rather than cross-state comparisons of absolute counts.
