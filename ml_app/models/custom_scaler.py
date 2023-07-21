import numpy as np
import pickle

class CustomScaler:
    """
    A custom scaler class that scales data using mean and standard deviation.

    Attributes:
    ----------
        means (numpy.ndarray): The means of the data.
        stds (numpy.ndarray): The standard deviations of the data.
    
    Methods:
    -------
        fit(data)
            Fits the scaler to the data.
        transform(data)
            Transforms the data using the scaler.
        fit_transform(data)
            Fits the scaler to the data and transforms the data.
    """

    def __init__(self) -> None:
        self.means = None
        self.stds = None

    def fit(self, data: np.ndarray) -> None:
        """
        Fits the scaler to the data.

        Args:
            data (numpy.ndarray): The data to fit the scaler to.
        """
        self.means = np.mean(data, axis=0)
        self.stds = np.std(data, axis=0)

    def transform(self, data: np.ndarray) -> np.ndarray:
        """
        Transforms the data using the scaler.

        Args:
            data (numpy.ndarray): The data to transform.

        Returns:
            numpy.ndarray: The transformed data.
        """
        return (data - self.means) / self.stds

    def fit_transform(self, data: np.ndarray) -> np.ndarray:
        """
        Fits the scaler to the data and transforms the data.

        Args:
            data (numpy.ndarray): The data to fit the scaler to and transform.

        Returns:
            numpy.ndarray: The transformed data.
        """
        self.fit(data)
        # Save the Scaler
        with open('datasets\\scaler.pkl', 'wb') as f:
            pickle.dump(self, f)
        return self.transform(data)