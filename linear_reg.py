from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
from main import GetDataFromCSV

# Step 1: Prepare your data
df = GetDataFromCSV("data2.csv").get_data()

df["datetime"] = pd.to_datetime(df["datetime"], format="%d.%m.%Y %H:%M")

# Ek özellikler çıkarma
df["day_of_week"] = df["datetime"].dt.day_name()  # Haftanın günü
df["hour"] = df["datetime"].dt.hour  # Saat
df["minute"] = df["datetime"].dt.minute  # Dakika
df["date"] = df["datetime"].dt.date
print(df)

#!!!!!!!!!!!!!!!!!!!!!!!!!!

# Haftanın günü bazında nöbet sıklığı
day_freq = df["day_of_week"].value_counts()
print(day_freq)

# Saat bazında nöbet sıklığı
hour_freq = df["hour"].value_counts()
print(hour_freq)

# Veri görselleştirme
import matplotlib.pyplot as plt

#!!!!!!!!!!!!!!!!!!!!

from prophet import Prophet

# Prophet için veri hazırlığı
prophet_df = df[["datetime"]].rename(columns={"datetime": "ds"})
prophet_df["y"] = df["hour"]  # Hedef değişken: Saat

# Model oluşturma ve eğitme
model = Prophet()
model.fit(prophet_df)

# Gelecekteki tarihler için tahmin
future = model.make_future_dataframe(periods=300, freq="D")
forecast = model.predict(future)

# Tahmini görselleştirme
model.plot(forecast)
plt.show()
