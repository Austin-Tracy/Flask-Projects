# Machine Learning Flask Web Application

This Flask web application provides a user-friendly interface to a diverse selection of machine learning models. By entering data into various forms, users can receive insightful predictions based on their unique inputs. The application features include:

## Home

The home page furnishes navigation to all the application's features.

## Models & Routes

The application currently supports a variety of machine learning models, each having its dedicated endpoint:

- **Logistic Regression** (`/logistic_regression`): Utilizes the `LogisticChurn` class to predict customer churn from various characteristics. The endpoint renders an HTML template displaying a form to input feature values and displays the predicted value.

- **Linear Regression** (`/linear_regression`): Deploys the `MonthlyChargeLinearRegression` class to predict a customer's monthly charge based on various characteristics. The endpoint returns an HTML template with a form for feature input and predicted value display.

- **K-Nearest Neighbors** (`/k_nearest_neighbors`): Uses the `ChurnKNN` class for predicting customer churn from various characteristics. The endpoint renders a page displaying the predicted class and the probability of user's input data.

- **Frequent Itemsets** (`/frequent_itemsets`): Applies the `get_product_rules` function to offer product recommendations based on the Apriori algorithm for frequent itemset mining and association rule learning. The item selection form is dynamically populated with a product list, and it provides the top 3 recommended items based on the selected item.

- **Sentiment Analysis** (`/sentiment_analysis`): Deploys the `analyze_sentiment` and `predict_sentiment` functions for text sentiment analysis. Predicted sentiment is displayed, and the text along with its sentiment is stored as session data.

- **Time Series Analysis** (`/time_series`): Employs an ARIMA model to predict future time series values. The endpoint renders the time series page and generates a forecast plot based on user input.

- **K-Means Clustering** (`/k_means_clustering`): Applies a `CustomScaler` and a trained K-Means model for customer segmentation. The endpoint renders the K-Means Clustering page, handles form submissions, standardizes form data, predicts clusters, and creates scatter plot data for each cluster.

- **Datasets** (`/datasets`): Renders a page displaying a dataset and its exploratory data analysis (EDA) generated by the `datasets` function.

## Datasets

Access to the dataset used to train the models is provided within the application. Feature descriptions elucidate the meaning of each feature in the dataset.

## Logging

Logging functionality is included in the application. Logs are recorded in a file named `stderr.log` located in the `ml_app/logs` directory, with the logging level set to DEBUG.

## Running the Application

To run the application, navigate to the root directory and use the following command:

```bash
flask run
```

## Future Work
Additional machine learning models and enhanced functionality will be incorporated into future versions of the application.

**Note**: This application is designed for educational and demonstration purposes. It should not be used for making actual predictions in a production environment.