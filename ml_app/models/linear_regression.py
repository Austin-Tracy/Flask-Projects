from sklearn.linear_model import LinearRegression
import numpy as np

class MonthlyChargeLinearRegression:
    """
    A class for performing linear regression on monthly charges data.

    Attributes:
    -----------
    model : LinearRegression
        A linear regression model from the scikit-learn library.

    Methods:
    --------
    train(X, y)
        Trains the linear regression model on the input data X and target values y.
    predict(X)
        Predicts the target values for the input data X using the trained model.
    load_model(model)
        Loads a pre-trained linear regression model.
    """
    def __init__(self) -> None:
        self.model = LinearRegression()

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Trains the linear regression model on the input data X and target values y.

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            The input data.
        y : array-like, shape (n_samples,)
            The target values.
        """
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predicts the target values for the input data X using the trained model.

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            The input data.

        Returns:
        --------
        y_pred : array-like, shape (n_samples,)
            The predicted target values.
        """
        return self.model.predict(X)

    def load_model(self, model: LinearRegression) -> None:
        """
        Loads a pre-trained linear regression model.

        Parameters:
        -----------
        model : LinearRegression
            A pre-trained linear regression model.
        """
        self.model = model