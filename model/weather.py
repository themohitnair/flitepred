import requests
import pandas as pd
from tqdm import tqdm

latitude = 40.6413
longitude = -73.7781

# Date range
start_date = "2024-01-01"
end_date = "2024-12-31"

url = (
    f"https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={latitude}&longitude={longitude}"
    f"&start_date={start_date}&end_date={end_date}"
    f"&hourly=temperature_2m,precipitation,cloudcover,windspeed_10m,weathercode"
    f"&timezone=America%2FNew_York"
)

print("📡 Fetching data from Open-Meteo...")
response = requests.get(url)
data = response.json()

print("📊 Processing rows...")
hourly_data = data["hourly"]
num_rows = len(hourly_data["time"])
rows = []

for i in tqdm(range(num_rows), desc="Building DataFrame"):
    row = {
        "time": hourly_data["time"][i],
        "temperature_2m": hourly_data["temperature_2m"][i],
        "precipitation": hourly_data["precipitation"][i],
        "cloudcover": hourly_data["cloudcover"][i],
        "windspeed_10m": hourly_data["windspeed_10m"][i],
        "weathercode": hourly_data["weathercode"][i],
    }
    rows.append(row)

df = pd.DataFrame(rows)
df["time"] = pd.to_datetime(df["time"])

output_file = "dataset/raw/jfk_hourly_weather_2024.csv"
df.to_csv(output_file, index=False)
print(f"✅ Done! Saved hourly weather to {output_file}")
