# nyla

A Machine Learning project that aims to create a model that predicts flight delays (classifies into on-time and delayed) based on data from the Bureau of Transportation Statistics (BTS) for flights from the JFK Airport, New York (NY) to the Los Angeles International Airport, Los Angeles (LA).

In aviation, a flight is officially considered “on time” if it arrives less than 15 minutes late compared to its scheduled arrival time.

## About the Data

- The dataset used for this project has been acquired from from the following source: [The Bureau of Transportation Statistics Website](https://transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr)
- Data from the years 2014 to 2024 (barring 2020 and 2021, owing to the addition of noise from the COVID-19 pandemic) was gathered, and it was analyzed for its two main categories: Destination and Airline Carrier. A total of 1044653 records were found, encompassing on-time performance data for all airports and airline carriers in the US from the BTS.
- After filtering to the routes AA, B6, and DL, a total of **89855** records were found.

### ✈️ Top 5 Destinations

| Destination ID | Flight Count |
| -------------- | ------------ |
| 12892          | 106,732      |
| 14771          | 70,681       |
| 10721          | 51,609       |
| 13204          | 45,952       |
| 13303          | 40,077       |

### 🛩️ Top 5 Airline Carriers

| Carrier | Flight Count |
| ------- | ------------ |
| B6      | 384,443      |
| DL      | 259,087      |
| AA      | 145,331      |
| 9E      | 103,118      |
| YX      | 60,349       |

### 🔁 Top 5 Routes (Carrier + Destination)

| Carrier | Destination ID | Flight Count |
| ------- | -------------- | ------------ |
| AA      | 12892          | 34,582       |
| B6      | 12892          | 28,599       |
| DL      | 12892          | 27,580       |
| B6      | 13204          | 26,635       |
| B6      | 11697          | 23,984       |

- AA (American Airlines), B6 (JetBlue Airlines), and DL (Delta Airlines) are found to be the top 3 carriers at the John F. Kennedy International Airport, New York.
- 12892 (Los Angeles International Airport, Los Angeles), 14771 (San Francisco International, San Francisco), and 10721 (Logan International Airport, Boston) are found to be the top 3 destinations from the John F. Kennedy International Airport, New York.
- The top 3 routes (routes being a unique combination of an Airline and a Destination) are all found to be to Los Angeles International Airport, Los Angeles, through the Top 3 Airline Carriers (Delta, JetBlue and American Airlines). The class imbalance among these is minimal, which is why it was decided to filter the data to the Top Destination (Los Angeles), and the Top 3 Airline Carriers.

## Feature Engineering

### Key Preprocessing & Feature Engineering (Script Logic)

1. **Column Renaming & Consistency**

   - Renamed columns to lowercase snake_case and logical names, e.g., `CRS_DEP_TIME` → `scheduled_departure_time`, `DEP_DELAY` → `departure_delay`, `OP_UNIQUE_CARRIER` → `carrier`.

2. **Critical Data Filtering**

   - Rows missing key flight info (`year`, `month`, `day_of_month`, `scheduled_departure_time`, `departure_delay`, `carrier`) were **dropped** like dead weight.

3. **Labeling**

   - `label`: Binary label – flights with positive `departure_delay` as `"delayed"`, others `"not_delayed"`.

4. **Departure Time Features**

   - `dep_min`: Departure time (`HHMM`) converted to **minutes since midnight**.
   - `dep_sin`, `dep_cos`: **Cyclical encoding** of departure time (think circular clocks).

5. **Departure Time Binning**

   - `departure_bin`: Departure time put into 4 bins:

     - `night` (0–359 min)
     - `morning` (360–719)
     - `afternoon` (720–1079)
     - `evening` (1080–1439)

6. **Day-of-Year Features**

   - `day_of_year`: Day of year (1–365/366).
   - `day_of_year_sin`, `day_of_year_cos`: Cyclical encoding of this day.

7. **Season Tagging**

   - `season`: Based on month (`spring`, `summer`, `fall`, `winter`).

8. **Holiday & Weekend**

   - `is_holiday_or_weekend`: **True** if flight on a **US holiday** or **weekend** (Saturday/Sunday).

9. **Part of Month**

   - `part_of_month_early`: True if day ≤ 10
   - `part_of_month_mid`: True if 11 ≤ day ≤ 20
   - `part_of_month_late`: True if day > 20

10. **One-Hot Encoding**

    - One-hot columns for:

      - `month` (12)
      - `day_of_week` (7)
      - `carrier` (all unique carriers)
      - `departure_bin` (4 bins)
      - `season` (4 seasons)

11. **Final Dataset Selection**

    - Kept:

      - **Direct features**: `scheduled_elapsed_time`, `label`, `dep_min`, `dep_sin`, `dep_cos`, `day_of_year_sin`, `day_of_year_cos`, `part_of_month_early`, `part_of_month_mid`, `part_of_month_late`, `is_holiday_or_weekend`
      - **One-hot features** for `month`, `day_of_week`, `carrier`, `departure_bin`, `season`.

This preprocessing pipeline effectively transforms raw flight data into a feature set ready for classification, with appropriate handling of temporal features, categorical variables, and the creation of a meaningful target variable.

## Class Imbalance

| Label       | Count | Percentage (%) |
| ----------- | ----- | -------------- |
| Not Delayed | 59991 | 66.76          |
| Delayed     | 29864 | 33.24          |

This table shows the class distribution after setting the delay threshold to 0 minutes. The classes are more or less balanced, with approximately a 2:1 ratio between not_delayed and delayed flights.
