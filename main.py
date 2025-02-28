import pandas as pd
from prophet import Prophet
from datetime import datetime
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import plotly.io as pio


class GetDataFromCSV:
    def __init__(self, path_way: str):
        self.header_names = ["datetime"]
        self.path_way = path_way

    def get_data(self) -> pd.DataFrame:
        return pd.read_csv(
            "data2.csv",
            parse_dates=self.header_names,
            dayfirst=True,
        )

    def prapare_data(self, df: pd.DataFrame = None) -> pd.DataFrame:
        df = df or self.get_data()
        df["datetime"] = pd.to_datetime(df["datetime"], dayfirst=True, utc=True)
        df["datetime"] = df["datetime"].dt.tz_convert(None)
        df.set_index("datetime", inplace=True)
        df["time"] = df.index.hour * 3600 + df.index.minute * 60
        return df


def forecast():
    # Prepare data
    df = GetDataFromCSV("data2.csv").prapare_data()
    # Ensure 'time' is numeric and drop NaN values
    df["time"] = pd.to_numeric(df["time"], errors="coerce")
    df = df.dropna(subset=["time"])  # Remove rows with NaN in 'time'

    # Initialize and fit the model
    model = ExponentialSmoothing(
        df["time"], trend="add", seasonal="add", seasonal_periods=4
    )
    fit = model.fit()

    # Forecast
    future_dates = pd.date_range(start=datetime.today(), periods=10, freq="D")
    predictions = fit.forecast(steps=len(future_dates))
    predictions = pd.DataFrame(
        predictions, index=future_dates, columns=["forecast_time(s)"]
    )

    # Convert forecasted time from seconds to hours:minutes:seconds
    predictions["forecast_time(h)"] = pd.to_datetime(
        predictions["forecast_time(s)"], unit="s"
    ).dt.strftime("%H:%M:%S")

    print(predictions)


def p_model():
    df = GetDataFromCSV("data2.csv").prapare_data()
    model = Prophet()
    model.fit(df)

    # Predict future
    future_dates = model.make_future_dataframe(
        periods=90, freq="D"
    )  # Predict next 30 days
    forecast = model.predict(future_dates)

    # Plot forecast
    model.plot(forecast)

    pio.renderers.default = "browser"

    print(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]])


if __name__ == "__main__":
    p_model()
