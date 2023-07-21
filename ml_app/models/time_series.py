import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from pandas.plotting import autocorrelation_plot

class TimeSeries:
    def __init__(self, p: int = 1, d: int = 1, q: int = 0, periods: int = 1) -> None:
        """
        Initializes a TimeSeries object with the given parameters.

        Args:
        p (int): The order of the autoregressive (AR) component of the model.
        d (int): The degree of differencing (I) to apply to the time series.
        q (int): The order of the moving average (MA) component of the model.
        periods (int): The number of periods to forecast into the future.
        """
        self.p = p
        self.d = d
        self.q = q
        self.periods = periods
        self.model = None
        self.forecast = None

    def train(self, data: pd.Series) -> None:
        """
        Trains the ARIMA model on the given time series data.

        Args:
        data (pandas.Series): The time series data to train the model on.
        """
        self.data = data
        self.model = ARIMA(self.data, order=(self.p, self.d, self.q))
        self.model_fit = self.model.fit(disp=0)

    def predict(self) -> None:
        """
        Generates a forecast for the time series based on the trained ARIMA model.
        """
        self.forecast = self.model_fit.predict(start=len(self.data), end=len(self.data)+self.periods-1)

    def load_model(self, model: ARIMA) -> None:
        """
        Loads a pre-trained ARIMA model.

        Args:
        model (statsmodels.tsa.arima.model.ARIMAResultsWrapper): The pre-trained ARIMA model to load.
        """
        self.model = model

    def acf_plot(self) -> None:
        """
        Generates an autocorrelation plot for the time series data.
        """
        autocorrelation_plot(self.data)