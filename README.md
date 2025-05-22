# nyla

A Machine Learning project that aims to create a model that predicts flight delays (classifies into on-time and delayed) based on data from the Bureau of Transportation Statistics (BTS) for flights from the JFK Airport, New York (NY) to the Los Angeles International Airport, Los Angeles (LA).

In aviation, a flight is officially considered “on time” if it arrives less than 15 minutes late compared to its scheduled arrival time.

## About the Data

- The dataset used for this project has been acquired from from the following source: [The Bureau of Transportation Statistics Website](https://transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr)
- Data from the years 2014 to 2024 (barring 2020 and 2021, owing to the addition of noise from the COVID-19 pandemic) was gathered, and it was analyzed for its two main categories: Destination and Airline Carrier. A total of 1044653 records were found, encompassing on-time performance data for all airports and airline carriers in the US from the BTS.

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

## Feature Engineering - Remastered Description

### Data Removal and Transformation

- Features such as Origin Airport ID, Destination Airport ID, Distance, and Year were removed as they were either constants (for a single NY to LA route) or irrelevant.
- CANCELLED and DIVERTED columns were also removed from the dataset.
- CRS_ELAPSED_TIME was renamed to scheduled_elapsed_time.

### Temporal Feature Engineering

- **Departure Time**: Transformed into three representations:
  - Raw minutes (dep_min)
  - Sinusoidal encoding (dep_sin, dep_cos) to capture cyclical nature of time
  - Categorical bins (departure_bin_night, departure_bin_morning, departure_bin_afternoon, departure_bin_evening)
- **Day of Week**: One-hot encoded into 7 columns (day_of_week_1 through day_of_week_7)
- **Day of Month**: Kept as raw numerical value
- **Month**: One-hot encoded into 12 columns (month_1 through month_12)

### Categorical Feature Engineering

- **Airline Carrier (OP_UNIQUE_CARRIER)**: One-hot encoded (carrier_AA, carrier_B6, carrier_DL)
- **is_holiday_or_weekend**: Boolean feature indicating whether the flight occurred on either a US holiday or weekend

### Target Variable Creation

- **Delay Classification (label)**:
  - "not_delayed": Negative Delay i.e., Delay less than 0 minutes
  - "delayed": Positive delay of 1 minute or more

This preprocessing pipeline effectively transforms raw flight data into a feature set ready for classification, with appropriate handling of temporal features, categorical variables, and the creation of a meaningful target variable.

Here's your data formatted as a neat markdown table:

| Label       | Count | Percentage (%) |
| ----------- | ----- | -------------- |
| Not Delayed | 59991 | 66.76          |
| Delayed     | 29864 | 33.24          |

This table shows the class distribution after setting the delay threshold to 0 minutes. The classes are more or less balanced, with approximately a 2:1 ratio between not_delayed and delayed flights.
