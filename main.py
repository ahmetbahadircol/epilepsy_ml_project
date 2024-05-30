import pandas as pd
from datetime import datetime
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# 1. Veri Hazırlama
data = {
    'Tarih': [
        '2023-05-01 14:00', '2023-05-02 15:00', '2023-05-03 14:30',
        '2023-05-04 16:00', '2023-05-05 14:00', '2023-05-06 15:00',
        '2023-05-07 14:30', '2023-05-08 16:00', '2023-05-09 14:00',
        '2023-05-10 15:00', '2023-05-11 14:30', '2023-05-12 16:00',
        '2023-05-13 14:00', '2023-05-14 15:00', '2023-05-15 14:30',
        '2023-05-16 16:00', '2023-05-17 14:00', '2023-05-18 15:00'
    ]
}

# 2. Veriyi Yükleme
df = pd.DataFrame(data)
df['Tarih'] = pd.to_datetime(df['Tarih'])
df.set_index('Tarih', inplace=True)

# 3. Veri Ön İşleme
# Saatleri saniye cinsinden dönüştürmek
df['Saat'] = df.index.hour * 3600 + df.index.minute * 60

# 4. Model Seçimi ve Eğitimi
# Basit bir Exponential Smoothing (Üstel Düzleştirme) modelini kullanıyoruz
model = ExponentialSmoothing(df['Saat'], seasonal='add', seasonal_periods=7)
fit = model.fit()

# 5. Tahmin
future_dates = pd.date_range(start='2023-05-19', periods=10, freq='D')
predictions = fit.forecast(steps=len(future_dates))
predictions = pd.DataFrame(predictions, index=future_dates, columns=['Tahmin Edilen Saat (saniye)'])

# Tahmin edilen saatleri tekrar saat formatına dönüştürmek
predictions['Tahmin Edilen Saat'] = pd.to_datetime(predictions['Tahmin Edilen Saat (saniye)'], unit='s').time

print(predictions)
