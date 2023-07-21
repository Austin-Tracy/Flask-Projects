import os
import pickle
import pytest
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from ml_app.models.custom_scaler import CustomScaler
from ml_app.models.eda import generate_EDA
from ml_app.models.frequent_itemsets import get_product_rules
from ml_app.models.k_nearest_neighbor import ChurnKNN
from ml_app.models.kmeans import KMeans
from ml_app.models.linear_regression import MonthlyChargeLinearRegression
from ml_app.models.logistic_regression import LogisticChurn, get_churn_model
from ml_app.models.sentiment_analysis import predict_sentiment
from ml_app.models.sia_sentiment import analyze_sentiment
from ml_app.models.time_series import TimeSeries

######## Time Series Tests ########
@pytest.fixture
def time_series():
    return TimeSeries(p=1, d=1, q=0, periods=1)

def test_train(time_series):
    data = pd.Series([1, 2, 3, 4, 5])
    time_series.train(data)
    assert isinstance(time_series.model, ARIMA)

def test_predict(time_series):
    data = pd.Series([1, 2, 3, 4, 5])
    time_series.train(data)
    time_series.predict()
    assert len(time_series.forecast) == time_series.periods

def test_load_model(time_series):
    data = pd.Series([1, 2, 3, 4, 5])
    model = ARIMA(data, order=(1, 1, 0)).fit(disp=0)
    time_series.load_model(model)
    assert time_series.model == model

def test_acf_plot(time_series):
    data = pd.Series([1, 2, 3, 4, 5])
    time_series.train(data)
    # Since acf_plot doesn't return anything, we can't assert anything here.
    # We just call it to make sure it doesn't raise an exception.
    time_series.acf_plot()


####### NLTK Sentiment Analysis Tests #######
def test_analyze_sentiment_positive():
    review = "This is a great product. I love it!"
    assert analyze_sentiment(review) == 'Positive'

def test_analyze_sentiment_negative():
    review = "This is a terrible product. I hate it!"
    assert analyze_sentiment(review) == 'Negative'

def test_analyze_sentiment_neutral():
    review = "This is a product."
    assert analyze_sentiment(review) == 'Neutral'


####### Sentiment Analysis Tests #######
def test_predict_sentiment_exists():
    assert callable(predict_sentiment)

def test_predict_sentiment_returns_string():
    sentiment = predict_sentiment("This is a test.")
    assert isinstance(sentiment, str)

def test_predict_sentiment_returns_positive_or_negative():
    sentiment = predict_sentiment("This is a test.")
    assert sentiment in ['Positive', 'Negative']

def test_predict_sentiment_identifies_positive():
    sentiment = predict_sentiment("This is a great product.")
    assert sentiment == 'Positive'

def test_predict_sentiment_identifies_negative():
    sentiment = predict_sentiment("This is a terrible product.")
    assert sentiment == 'Negative'

###### Logistic Regression Tests ######
@pytest.fixture
def churn_model():
    return LogisticChurn()

def test_init(churn_model):
    assert isinstance(churn_model.data, pd.DataFrame)
    assert churn_model.target == 'Churn'
    assert churn_model.trained_model is None
    assert churn_model.model_equation is None

def test_clean(churn_model):
    churn_model.clean()
    assert churn_model.data[churn_model.target].isin([0, 1]).all()

def test_eda(churn_model):
    churn_model.eda()
    with open('ml_app\\ml_models\\static\\json\\scatter_matrix.json', 'r') as f:
        assert f.read() is not None

def test_feature_selection(churn_model):
    churn_model.feature_selection()
    assert set(churn_model.data.columns) == set(churn_model.features + [churn_model.target])

def test_train(churn_model):
    churn_model.train()
    assert churn_model.trained_model is not None
    assert churn_model.model_equation is not None

def test_analysis(churn_model):
    headers, data = churn_model.analysis()
    assert headers is not None
    assert data is not None

def test_predict(churn_model):
    X_values = churn_model.data[churn_model.features].head(1)
    prediction = churn_model.predict(X_values)
    assert prediction is not None

def test_headers_and_rows(churn_model):
    headers, data = churn_model.headers_and_rows()
    assert headers is not None
    assert data is not None

def test_get_churn_model():
    churn_model, headers, data, _, _ = get_churn_model()
    assert isinstance(churn_model, LogisticChurn)
    assert headers is not None
    assert data is not None

####### Linear Regression Tests #######
@pytest.fixture
def regression_model():
    return MonthlyChargeLinearRegression()

def test_init(regression_model):
    assert isinstance(regression_model.model, LinearRegression)

def test_train(regression_model):
    X = np.random.rand(10, 1)
    y = np.random.rand(10)
    regression_model.train(X, y)
    assert regression_model.model.coef_ is not None
    assert regression_model.model.intercept_ is not None

def test_predict(regression_model):
    X = np.random.rand(10, 1)
    y = np.random.rand(10)
    regression_model.train(X, y)
    predictions = regression_model.predict(X)
    assert predictions.shape == (10,)

def test_load_model(regression_model):
    new_model = LinearRegression()
    X = np.random.rand(10, 1)
    y = np.random.rand(10)
    new_model.fit(X, y)
    regression_model.load_model(new_model)
    assert np.allclose(regression_model.model.coef_, new_model.coef_)
    assert np.isclose(regression_model.model.intercept_, new_model.intercept_)

###### KMeans Tests ######
@pytest.fixture
def kmeans():
    return KMeans(K=2)

def test_closest_centroid(kmeans):
    kmeans.centroids = np.array([[0, 0], [1, 1]])
    sample = np.array([0.5, 0.5])
    assert kmeans._closest_centroid(sample, kmeans.centroids) == 1

def test_create_clusters(kmeans):
    kmeans.centroids = np.array([[0, 0], [1, 1]])
    kmeans.X = np.array([[0, 0], [1, 1], [0.1, 0.1], [0.9, 0.9]])
    assert kmeans._create_clusters(kmeans.centroids) == [[0, 2], [1, 3]]

def test_get_centroids(kmeans):
    kmeans.X = np.array([[0, 0], [1, 1], [0.1, 0.1], [0.9, 0.9]])
    clusters = [[0, 2], [1, 3]]
    assert np.array_equal(kmeans._get_centroids(clusters), np.array([[0.05, 0.05], [0.95, 0.95]]))

def test_is_converged(kmeans):
    centroids_old = np.array([[0, 0], [1, 1]])
    centroids_new1 = np.array([[0, 0], [1, 1]])
    centroids_new2 = np.array([[0.1, 0.1], [0.9, 0.9]])
    assert kmeans._is_converged(centroids_old, centroids_new1) == True
    assert kmeans._is_converged(centroids_old, centroids_new2) == False

def test_predict(kmeans):
    kmeans.centroids = np.array([[0, 0], [1, 1]])
    X = np.array([[0, 0], [1, 1], [0.1, 0.1], [0.9, 0.9]])
    assert np.array_equal(kmeans.predict(X), np.array([0, 1, 0, 1]))

def test_calculate_WCSS(kmeans):
    kmeans.X = np.array([[0, 0], [1, 1], [0.1, 0.1], [0.9, 0.9]])
    kmeans.centroids = np.array([[0, 0], [1, 1]])
    kmeans.clusters = [[0, 2], [1, 3]]
    assert kmeans.calculate_WCSS() == 0.04

####### KNN Tests #######
@pytest.fixture
def churn_knn():
    return ChurnKNN(n_neighbors=3)

def test_init(churn_knn):
    assert isinstance(churn_knn.model, KNeighborsClassifier)
    assert churn_knn.model.n_neighbors == 3

def test_train(churn_knn):
    X_train = np.array([[1, 2], [3, 4], [5, 6]])
    y_train = np.array([0, 1, 0])
    churn_knn.train(X_train, y_train)
    assert churn_knn.model.classes_.tolist() == [0, 1]

def test_predict(churn_knn):
    X_test = np.array([[1, 2], [3, 4]])
    churn_knn.model.fit(np.array([[1, 2], [3, 4], [5, 6]]), np.array([0, 1, 0]))
    predictions = churn_knn.predict(X_test)
    assert predictions.shape == X_test.shape[0]

def test_predict_proba(churn_knn):
    X_test = np.array([[1, 2], [3, 4]])
    churn_knn.model.fit(np.array([[1, 2], [3, 4], [5, 6]]), np.array([0, 1, 0]))
    probabilities = churn_knn.predict_proba(X_test)
    assert probabilities.shape == (X_test.shape[0], churn_knn.model.classes_.size)

def test_load_model(churn_knn):
    new_model = KNeighborsClassifier(n_neighbors=7)
    churn_knn.load_model(new_model)
    assert churn_knn.model.n_neighbors == 7


####### Frequent Itemsets Tests #######
def test_get_product_rules_returns_tuple():
    result = get_product_rules()
    assert isinstance(result, tuple), "Expected a tuple"

def test_get_product_rules_first_element_dataframe():
    result = get_product_rules()
    assert isinstance(result[0], pd.DataFrame), "Expected a DataFrame"

def test_get_product_rules_second_element_list():
    result = get_product_rules()
    assert isinstance(result[1], list), "Expected a list"

def test_get_product_rules_dataframe_columns():
    result = get_product_rules()
    expected_columns = ['antecedents', 'consequents', 'antecedent support', 'consequent support', 'support', 'confidence', 'lift', 'leverage', 'conviction']
    assert list(result[0].columns) == expected_columns, "Unexpected DataFrame columns"

def test_get_product_rules_no_same_antecedent_consequent():
    result = get_product_rules()
    assert not any(result[0]['antecedents'] == result[0]['consequents']), "Found rows with same antecedent and consequent"

def test_get_product_rules_no_dust_off_compressed_gas():
    result = get_product_rules()
    assert not any(result[0]['antecedents'].apply(lambda x: 'Dust-Off Compressed Gas 2 pack' in x)), "Found rows with 'Dust-Off Compressed Gas 2 pack' as antecedent"

###### EDA Tests ######
@pytest.fixture
def sample_df():
    data = {
        'feature1': ['A', 'B', 'A', 'B', 'A'],
        'feature2': [1, 2, 3, 4, 5],
        'target': ['X', 'Y', 'X', 'Y', 'X']
    }
    df = pd.DataFrame(data)
    return df

def test_generate_EDA(sample_df):
    feature_vars = ['feature1', 'feature2']
    target_var = 'target'
    result = generate_EDA(sample_df, feature_vars, target_var)
    
    assert isinstance(result, dict)
    assert len(result) == len(feature_vars)
    for feature in feature_vars:
        assert feature in result
        assert isinstance(result[feature], str)


###### CustomScaler Tests ######
@pytest.fixture
def scaler():
    return CustomScaler()

def test_fit(scaler):
    data = np.array([[1, 2], [3, 4], [5, 6]])
    scaler.fit(data)
    assert np.allclose(scaler.means, np.array([3, 4]))
    assert np.allclose(scaler.stds, np.array([1.63299316, 1.63299316]))

def test_transform(scaler):
    data = np.array([[1, 2], [3, 4], [5, 6]])
    scaler.fit(data)
    transformed_data = scaler.transform(data)
    assert np.allclose(transformed_data, np.array([[-1.22474487, -1.22474487], [0, 0], [1.22474487, 1.22474487]]))

def test_fit_transform(scaler):
    data = np.array([[1, 2], [3, 4], [5, 6]])
    transformed_data = scaler.fit_transform(data)
    assert np.allclose(transformed_data, np.array([[-1.22474487, -1.22474487], [0, 0], [1.22474487, 1.22474487]]))

def test_save_scaler(scaler):
    data = np.array([[1, 2], [3, 4], [5, 6]])
    scaler.fit_transform(data)
    assert os.path.exists('datasets\\scaler.pkl')
    with open('datasets\\scaler.pkl', 'rb') as f:
        loaded_scaler = pickle.load(f)
    assert np.allclose(loaded_scaler.means, np.array([3, 4]))
    assert np.allclose(loaded_scaler.stds, np.array([1.63299316, 1.63299316]))

def test_load_scaler(scaler):
    data = np.array([[1, 2], [3, 4], [5, 6]])
    scaler.fit_transform(data)
    with open('datasets\\scaler.pkl', 'rb') as f:
        loaded_scaler = pickle.load(f)
    assert np.allclose(loaded_scaler.means, np.array([3, 4]))
    assert np.allclose(loaded_scaler.stds, np.array([1.63299316, 1.63299316]))
    loaded_transformed_data = loaded_scaler.transform(data)
    assert np.allclose(loaded_transformed_data, np.array([[-1.22474487, -1.22474487], [0, 0], [1.22474487, 1.22474487]]))
