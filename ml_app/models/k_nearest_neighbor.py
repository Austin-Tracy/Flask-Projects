from sklearn.neighbors import KNeighborsClassifier
import numpy as np

class ChurnKNN:
    """
    A class that represents a KNN classifier for predicting customer churn.
    """
    def __init__(self, n_neighbors: int = 5) -> None:
        """
        Initializes a KNN classifier with the specified number of neighbors.

        Args:
        n_neighbors (int): The number of neighbors to use for classification. Default is 5.
        """
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors)

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Trains the KNN classifier on the given training data.

        Args:
        X (array-like): The training data features.
        y (array-like): The training data labels.
        """
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predicts the class labels for the given test data.

        Args:
        X (array-like): The test data features.

        Returns:
        array-like: The predicted class labels.
        """
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predicts the class probabilities for the given test data.

        Args:
        X (array-like): The test data features.

        Returns:
        array-like: The predicted class probabilities.
        """
        return self.model.predict_proba(X)

    def load_model(self, model: KNeighborsClassifier) -> None:
        """
        Loads a pre-trained KNN classifier model.

        Args:
        model (KNeighborsClassifier): The pre-trained KNN classifier model.
        """
        self.model = model