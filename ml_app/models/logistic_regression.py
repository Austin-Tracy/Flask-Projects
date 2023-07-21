# ml_app/blueprints/models/logistic_regression.py
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pickle
import statsmodels.api as sm
import json
import plotly
import plotly.express as px

class LogisticChurn:
    """
    A class that represents a logistic regression model for predicting customer churn.

    Attributes:
    -----------
    - data: A pandas DataFrame containing the cleaned dataset.
    - target: A string representing the target variable column name.
    - features: A pandas DataFrame containing the selected features.
    - trained_model: A trained logistic regression model.
    - model_equation: The equation of the trained logistic regression model.

    Methods:
    --------
    - clean(): Cleans the dataset by converting the target variable to binary.
    - eda(): Performs exploratory data analysis by creating a scatter matrix plot.
    - feature_selection(): Selects the features to be used in the model.
    - train(): Trains the logistic regression model and saves it to a pickle file.
    - analysis(): Performs statistical analysis on the trained model.
    - predict(X_values): Predicts the target variable for the given input values.
    - headers_and_rows(): Returns the column headers and the first 100 rows of the dataset.
    """

    def __init__(self) -> None:
        """
        Initializes the LogisticChurn class with the dataset, target variable, selected features, trained model, and model equation.
        """
        self.data = pd.read_csv(os.path.join('ml_app', 'models', 'datasets', 'churn_clean.csv'))
        self.data = self.data.dropna()
        self.data = self.data.replace(to_replace={'Yes': 1, 'No': 0})
        self.target = 'Churn'
        self.features = self.data[['Children', 'Age', 'Contacts', 'Yearly_equip_failure', 'Techie',
       'Port_modem', 'Tablet', 'Multiple', 'OnlineSecurity', 'OnlineBackup',
       'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
       'PaperlessBilling', 'PaymentMethod']]
        self.trained_model = None
        self.model_equation = None

    def clean(self) -> None:
        """
        Cleans the dataset by converting the target variable to binary.
        """
        self.data[self.target] = self.data[self.target].apply(lambda x: 1 if x == 'Yes' else 0)

    def eda(self) -> None:
        """
        Performs exploratory data analysis by creating a scatter matrix plot.
        """
        fig = px.scatter_matrix(self.data, dimensions=self.data.columns, color=self.target)
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        file_path = os.path.join('ml_app', 'models', 'static', 'json', 'scatter_matrix.json')
        with open(file_path, 'w') as f:
            f.write(plot_json)

    def feature_selection(self) -> None:
        """
        Selects the features to be used in the model.
        """
        if self.features is not None:
            self.data = self.data[self.features + [self.target]]

    def train(self) -> None:
        """
        Trains the logistic regression model and saves it to a pickle file.
        """
        X = pd.get_dummies(self.features)
        y = self.data[self.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LogisticRegression(max_iter=100000)
        model.fit(X_train, y_train)
        model_path = os.path.join('ml_app', 'trained_models', 'logistic_regression.pkl')
        with open(model_path, 'wb') as model_file:
            pickle.dump(model, model_file)
        self.trained_model = model
        self.model_equation = model.coef_
        predicted = model.predict(X_test)
        print(metrics.classification_report(y_test, predicted))

    def analysis(self) -> tuple:
        """
        Performs statistical analysis on the trained model.
        """
        if self.trained_model is None:
            print("Model is not trained yet.")
            return None
        X = self.features
        X = pd.get_dummies(X)
        X = X.astype(int)
        X = sm.add_constant(X)
        y = self.data[self.target]
        logit_model = sm.Logit(y, X)
        result = logit_model.fit()
        summary = result.summary()
        summary_str = str(summary.tables[1]).strip()
        summary_table = [row.split() for row in summary_str.split('\n')]
        headers = summary_table.pop(1)
        summary_table = summary_table[2:-1]
        data = summary_table
        return headers, data

    def predict(self, X_values) -> np.ndarray:
        """
        Predicts the target variable for the given input values.

        Args:
        - X_values: A pandas DataFrame containing the input values.

        Returns:
        - The predicted target variable values.
        """
        if self.trained_model is None:
            print("Model is not trained yet.")
            return None
        return self.trained_model.predict(X_values)

    def headers_and_rows(self) -> tuple:
        """
        Returns the column headers and the first 100 rows of the dataset.

        Returns:
        - The column headers and the first 100 rows of the dataset.
        """
        return self.data.columns, self.data.head(100).values
    
def get_churn_model() -> tuple:
    """
    Returns the trained logistic regression model, column headers, and the first 100 rows of the dataset.

    Returns:
    - The trained logistic regression model, column headers, and the first 100 rows of the dataset.
    """
    churn_model = LogisticChurn()
    model_path = os.path.join('ml_app', 'trained_models', 'logistic_regression.pkl')
    try:
        with open(model_path, 'rb') as model_file:
            loaded_model = pickle.load(model_file)
        churn_model.trained_model = loaded_model
        print("Loaded the model from the pickle file.")
    except FileNotFoundError:
        print("Could not find the model file. Please ensure the file path is correct.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    headers, data = churn_model.headers_and_rows()
    return churn_model, headers, data, None, None
