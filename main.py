import pandas as pd
from datetime import datetime
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class GetDataFromCSV:
    def __init__(self, path_way: str):
        self.header_names = ["name", "begin_date", "end_date"]
        self.path_way = path_way
        
    def get_data(self) -> pd.DataFrame:
        return pd.read_csv(self.path_way, on_bad_lines="skip", header=None, names=self.header_names)

    def prapare_data(self, df: pd.DataFrame=None) -> pd.DataFrame:
        df = df or self.get_data()
        df['begin_date'] = pd.to_datetime(df['begin_date'])
        # df['date'] = df['begin_date'].dt.date
        # df['time'] = df['begin_date'].dt.time
        df.drop(columns=["name", "end_date"], inplace=True)
        df.set_index('begin_date', inplace=True)
        df['time'] = df.index.hour * 3600 + df.index.minute * 60
        return df


def forecast():
    df = GetDataFromCSV("data.csv").prapare_data()

    # Exponential Smoothing
    print(df)
    model = ExponentialSmoothing(df['time'], trend='add', seasonal='add', seasonal_periods=4)
    fit = model.fit()

    # Forecast
    future_dates = pd.date_range(start=datetime.today(), periods=10, freq='D')
    predictions = fit.forecast(steps=len(future_dates))
    predictions = pd.DataFrame(predictions, index=future_dates, columns=['forecast_time(s)'])
    breakpoint()

    predictions['forecast_time(h)'] = pd.to_datetime(predictions['forecast_time(s)'], unit='s').time

    print(predictions)


# print(GetDataFromCSV("data.csv").prapare_data())
forecast()
