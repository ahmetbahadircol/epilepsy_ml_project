import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
from main import GetDataFromCSV

# Step 1: Prepare your data
df = GetDataFromCSV("data2.csv").get_data()

# Create a DataFrame
df["datetime"] = pd.to_datetime(df["datetime"], format="%d.%m.%Y %H:%M")

# Extract date and time
df["date"] = df["datetime"].dt.date
df["time"] = df["datetime"].dt.time

# Convert date to ordinal (numerical value for regression)
df["date_ordinal"] = df["date"].apply(lambda x: x.toordinal())

# Convert time to total seconds since midnight for plotting
df["time_seconds"] = df["datetime"].dt.hour * 3600 + df["datetime"].dt.minute * 60

# Fit Exponential Smoothing model
model = ExponentialSmoothing(df["date_ordinal"], trend="add", seasonal=None)
fit = model.fit()

# Forecast future dates
future_dates = pd.date_range(start=df["datetime"].iloc[-1], periods=10, freq="D")
future_ordinal = fit.forecast(steps=len(future_dates))

# Convert predicted dates from ordinal to actual date format
predicted_dates = [pd.Timestamp.fromordinal(int(val)).date() for val in future_ordinal]

# Use the average observed time (in seconds) for predictions
average_time_seconds = df["time_seconds"].mean()

# Prepare for plotting
plt.figure(figsize=(12, 6))

# Plot observed data
plt.scatter(df["date"], df["time_seconds"], label="Observed", color="blue")

# Plot predicted data
plt.scatter(
    predicted_dates,
    [average_time_seconds] * len(predicted_dates),
    label="Predicted",
    color="red",
)

# Customize the y-axis to display time in HH:MM format
y_ticks = plt.gca().get_yticks()
y_labels = [f"{int(tick // 3600):02}:{int((tick % 3600) // 60):02}" for tick in y_ticks]
plt.gca().set_yticklabels(y_labels)

# Customize the plot
plt.xlabel("Date (dd.mm.yyyy)")
plt.ylabel("Time (HH:MM)")
plt.title("Seizure Prediction")
plt.legend()

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

plt.show()
