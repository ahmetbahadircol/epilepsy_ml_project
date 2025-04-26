import pandas as pd
import matplotlib.pyplot as plt

# Read the data from CSV
df = pd.read_csv("data.csv")

# Ensure the datetime column is in datetime format, handling errors
df["datetime"] = pd.to_datetime(
    df["datetime"].str.strip(), format="%d.%m.%Y %H:%M", errors="coerce"
)

# Calculate day differences between seizures
df["days_since_last_seizure"] = df["datetime"].diff().dt.total_seconds() / (3600 * 24)

# Drop the first row because its difference is NaN
df = df.dropna()

# Format dates nicely for x-axis
date_labels = df["datetime"].dt.strftime("%d-%m-%Y")

# Plot
plt.figure(figsize=(14, 7))
bars = plt.bar(
    date_labels, df["days_since_last_seizure"], color="skyblue", edgecolor="black"
)

plt.xlabel("Seizure Date")
plt.ylabel("Days Since Last Seizure")
plt.title("Days Between Each Seizure")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.xticks(rotation=90, fontsize=8)
plt.tight_layout()

# Add the number on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        yval + 0.5,
        f"{yval:.0f}",
        ha="center",
        va="bottom",
        fontsize=8,
    )

plt.show()
