# nyla

A Machine Learning project that predicts flight delays at JFK Airport using historical flight data from the Bureau of Transportation Statistics (BTS) combined with weather data from the Iowa Environmental Mesonet. The model classifies flights as either "delayed" (departure delay > 0 minutes) or "not_delayed" based on comprehensive flight and weather features.

## Data Pipeline Overview

The project follows a structured data processing pipeline with the following stages:

### **Pipeline Flow**

```
Raw Data → Amalgamate → Analyze → Filter → Prune → Weather Processing → Optimize → Impute → **Ready**
```

| Script          | Input                                        | Output                                          | Purpose                                                                 |
| --------------- | -------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------- |
| `amalgamate.py` | `dataset/raw/*.csv`                          | `dataset/processed/jfk_combined.csv`            | Combines all raw flight CSV files, filtering for JFK origin (ID: 12478) |
| `stats.py`      | `jfk_combined.csv`                           | Analysis results                                | Analyzes top destinations, carriers, and routes                         |
| `filter.py`     | `jfk_combined.csv`                           | `dataset/processed/airline_filtered.csv`        | Filters for top 3 carriers (AA, B6, DL) and LAX destination (ID: 12892) |
| `prune.py`      | `airline_filtered.csv`                       | `dataset/processed/airline_filtered_pruned.csv` | Removes cancelled/diverted flights, cleans columns                      |
| `augment.py`    | `dataset/raw/weather_2014_2024.csv`          | `dataset/processed/jfk_weather_processed.csv`   | Processes weather data with feature engineering                         |
| `optimize.py`   | `airline_filtered_pruned.csv` + weather data | `dataset/processed/jfk_optimized.csv`           | Merges flight and weather data, creates ML features                     |
| `impute.py`     | `jfk_optimized.csv`                          | `jfk_optimized_clean.csv`                       | Handles missing values and final cleaning                               |

### **Execution Scripts**

- **`pipeline.py`**: Runs the complete pipeline from raw data to ML-ready dataset
- **`main.py`**: Quick execution of the imputation step with data quality checks

## About the Data

### **Flight Data Source**

- **Source**: [Bureau of Transportation Statistics](https://transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr)
- **Time Period**: 2014-2024 (excluding 2020-2021 due to COVID-19 impact)
- **Origin Airport**: JFK International Airport (ID: 12478)
- **Target Route**: JFK → Los Angeles International Airport (ID: 12892)
- **Selected Carriers**: American Airlines (AA), JetBlue (B6), Delta Airlines (DL)

### **Weather Data Source**

- **Source**: [Iowa Environmental Mesonet](https://mesonet.agron.iastate.edu/request/download.phtml?network=NY_ASOS)
- **Station**: JFK Airport weather station
- **Coverage**: 2014-2024 (excluding 2020-2021)
- **Records**: 96,389 weather observations

## Data Analysis Results

### **Top Destinations from JFK**

| Destination ID | Airport                           | Flight Count |
| -------------- | --------------------------------- | ------------ |
| 12892          | Los Angeles International (LAX)   | 106,732      |
| 14771          | San Francisco International (SFO) | 70,681       |
| 10721          | Logan International (BOS)         | 51,609       |
| 13204          | Fort Lauderdale-Hollywood         | 45,952       |
| 13303          | Orlando International             | 40,077       |

### **Top Airline Carriers at JFK**

| Carrier | Airline           | Flight Count |
| ------- | ----------------- | ------------ |
| B6      | JetBlue Airways   | 384,443      |
| DL      | Delta Air Lines   | 259,087      |
| AA      | American Airlines | 145,331      |
| 9E      | Endeavor Air      | 103,118      |
| YX      | Republic Airways  | 60,349       |

### **Selected Route Analysis (JFK → LAX)**

| Carrier | Flight Count | Percentage |
| ------- | ------------ | ---------- |
| AA      | 34,582       | 38.5%      |
| B6      | 28,599       | 31.8%      |
| DL      | 27,580       | 30.7%      |

**Final Filtered Dataset**: 89,855 records for the JFK→LAX route across the three major carriers.

## Weather Data Processing

### **Weather Features Engineered**

**Basic Meteorological Data:**

- Temperature (Celsius), wind direction/speed, pressure, visibility
- Precipitation amount and type detection from METAR reports
- Cloud coverage and ceiling height calculations

**Aviation-Specific Features:**

- **Crosswind Component**: Calculated for JFK's primary runway (heading 40°)
- **IFR Conditions**: Ceiling < 1000ft OR visibility < 3 miles
- **MVFR Conditions**: Marginal VFR conditions
- **Weather Phenomena**: Extracted from METAR (rain, snow, fog, thunderstorms, etc.)

**Categorical Features:**

- Wind speed categories (calm, light, moderate, strong)
- Visibility categories (very_poor to excellent)
- Precipitation categories (none, trace, light, heavy)
- Pressure categories (very_low, low, normal, high)

### **Weather Data Quality**

- **Missing Data**: < 1% for critical weather parameters
- **Weather Matching**: Flight times matched to nearest weather observation (±2 hours)
- **Weather Types Detected**: 20+ different weather phenomena from METAR reports

## Feature Engineering Pipeline

### **Temporal Features**

- **Cyclical Time Encoding**: Sine/cosine transformations for departure time and day of year
- **Departure Time Bins**: Night, morning, afternoon, evening
- **Seasonal Features**: Spring, summer, fall, winter
- **Calendar Features**: Holiday/weekend detection, part of month (early/mid/late)

### **Flight-Specific Features**

- **Carrier Encoding**: One-hot encoding for AA, B6, DL
- **Scheduled Elapsed Time**: Flight duration
- **Day of Week**: Monday through Sunday encoding

### **Weather Integration**

- **Real-time Matching**: Each flight matched to closest weather observation
- **Comprehensive Weather State**: 50+ weather-related features per flight
- **Aviation Weather Standards**: IFR/MVFR conditions following FAA guidelines

## Target Variable & Class Distribution

**Delay Definition**: Flights with departure delay > 0 minutes are classified as "delayed"

| Class       | Count  | Percentage |
| ----------- | ------ | ---------- |
| Not Delayed | 59,991 | 66.76%     |
| Delayed     | 29,864 | 33.24%     |

The dataset shows a reasonable class balance with a 2:1 ratio, eliminating the need for aggressive resampling techniques.

## Data Quality Assessment

**Final Dataset Dimensions**: 89,830 rows × 99 columns

### **Missing Value Summary**

- **Total Missing Values**: 5,164 (0.058% of all data points)
- **Primary Missing Columns**:
  - `cloud_height`: 3.19% (handled with median imputation)
  - `wind_direction`: 1.00% (handled with median imputation)
  - Other weather parameters: < 0.2% missing

### **Data Completeness Strategy**

1. **Critical Weather Imputation**: Cloud height and wind direction filled with median values
2. **Crosswind Recalculation**: Updated after wind direction imputation
3. **Complete Case Analysis**: Remaining rows with missing values removed
4. **Final Result**: 100% complete dataset ready for machine learning

## Technical Implementation

### **Key Scripts Functionality**

**Data Collection & Filtering:**

- `amalgamate.py`: Recursively collects and combines CSV files, filters by origin airport
- `filter.py`: Applies business logic filters (carriers, destinations)
- `prune.py`: Removes cancelled/diverted flights, standardizes column names

**Feature Engineering:**

- `augment.py`: Comprehensive weather data processing with METAR parsing
- `optimize.py`: Temporal feature creation, weather-flight data merging
- `impute.py`: Final data cleaning and missing value handling

**Analysis & Validation:**

- `stats.py`: Statistical analysis of routes, carriers, and destinations
- Built-in data quality checks throughout the pipeline

The pipeline produces a clean, feature-rich dataset optimized for machine learning classification tasks, combining aviation domain knowledge with comprehensive weather integration for accurate flight delay prediction.
