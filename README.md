# flitepred

A Machine Learning project that aims to create a model that predicts flight delays (classifies into on-time and delayed) based on data from the Bureau of Transportation Statistics (BTS) for flights from the JFK Airport in New York City to the Los Angeles International Airport, Los Angeles.

In aviation, a flight is officially considered “on time” if it arrives less than 15 minutes late compared to its scheduled arrival time.

## About the Data

- The dataset used for this project has been acquired from from the following source: [The Bureau of Transportation Statistics Website](https://transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr)
- Data from the years 2014 to 2024 (barring 2020 and 2019, owing to the addition of noise from the COVID-19 pandemic) was gathered, and it was analyzed for its two main categories: Destination and Airline Carrier.

### ✈️ Top 5 Destinations

| Destination ID | Flight Count |
| -------------- | ------------ |
| 12892          | 106,732      |
| 14771          | 70,681       |
| 10721          | 51,609       |
| 13204          | 45,952       |
| 13303          | 40,077       |

---

### 🛩️ Top 5 Airline Carriers

| Carrier | Flight Count |
| ------- | ------------ |
| B6      | 384,443      |
| DL      | 259,087      |
| AA      | 145,331      |
| 9E      | 103,118      |
| YX      | 60,349       |

---

### 🔁 Top 5 Routes (Carrier + Destination)

| Carrier | Destination ID | Flight Count |
| ------- | -------------- | ------------ |
| AA      | 12892          | 34,582       |
| B6      | 12892          | 28,599       |
| DL      | 12892          | 27,580       |
| B6      | 13204          | 26,635       |
| B6      | 11697          | 23,984       |

- AA (American Airlines), B6 (JetBlue Airlines), and DL (Delta Airlines) are found to be the top 3 carriers at the John F. Kennedy International Airport, New York.
- 12892 (Los Angeles International Airport, Los Angeles), 14771 (San Francisco International, San Francisco), and (Logan International Airport, Boston) are found to be the top 3 destinations from the John F. Kennedy International Airport, New York.
- The top 3 routes (routes being a unique combination of an Airline and a Destination) are all found to be to Los Angeles International Airport, Los Angeles, through the Top 3 Airline Carriers (Delta, JetBlue and American Airlines). The class imbalance among these is minimal, which is why it was decided to filter the data to the Top Destination (Los Angeles), and the Top 3 Airline Carriers.
