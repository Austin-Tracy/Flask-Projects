import pytest
from flask import Flask, url_for, session
from gpt_app.blueprints.routes import k_means_clustering, datasets
from unittest.mock import patch, MagicMock
from pm_app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_logistic_regression_get(client):
    response = client.get(url_for('logistic_regression'))
    assert response.status_code == 200

def test_logistic_regression_post_valid(client):
    form_data = {
        # Fill in with valid form data
    }
    response = client.post(url_for('logistic_regression'), data=form_data)
    assert response.status_code == 200
    # Add assertion to check the prediction in the response

def test_logistic_regression_post_invalid(client):
    form_data = {
        # Fill in with invalid form data
    }
    response = client.post(url_for('logistic_regression'), data=form_data)
    assert response.status_code == 400

def test_linear_regression_get(client):
    response = client.get(url_for('linear_regression'))
    assert response.status_code == 200

def test_linear_regression_post_valid(client):
    form_data = {
        # Fill in with valid form data
    }
    response = client.post(url_for('linear_regression'), data=form_data)
    assert response.status_code == 200
    # Add assertion to check the prediction in the response

def test_linear_regression_post_invalid(client):
    form_data = {
        # Fill in with invalid form data
    }
    response = client.post(url_for('linear_regression'), data=form_data)
    assert response.status_code == 400

def test_k_nearest_neighbors(client):
    mock_form_data = {
        'Techie': 'Yes',
        'Multiple': 'Yes',
        'OnlineBackup': 'Yes',
        'DeviceProtection': 'Yes',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'Yes',
        'Tenure': 12,
        'MonthlyCharge': 100,
        'Bandwidth_GB_Year': 500,
        'InternetService': 'DSL',
        'Contract': 'Month-to-month'
    }
    response = client.post(url_for('ml_app.k_nearest_neighbors'), data=mock_form_data)
    assert response.status_code == 200
    assert b"Customer will Churn" in response.data

def test_frequent_itemsets(client):
    mock_form_data = {
        'item': 'Product1'
    }
    response = client.post(url_for('ml_app.frequent_itemsets'), data=mock_form_data)
    assert response.status_code == 200
    assert b"Product1" in response.data


def test_sentiment_analysis(client):
    response = client.get('/sentiment_analysis')
    assert response.status_code == 200
    assert b"Sentiment Analysis" in response.data

    response = client.post('/sentiment_analysis', data={'text': 'I love this product!'})
    assert response.status_code == 200
    assert session.get('sentiment_history') is not None

def test_time_series(client):
    response = client.get('/time_series')
    assert response.status_code == 200
    assert b"Time Series Analysis" in response.data

    response = client.post('/time_series', data={'periods': 7})
    assert response.status_code == 200
    assert session.get('forecast_history') is not None

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('blueprints.routes.KMeansClusteringForm')
@patch('blueprints.routes.KMeans')
@patch('blueprints.routes.CustomScaler')
@patch('blueprints.routes.pd.read_csv')
def test_k_means_clustering(mock_form, mock_kmeans, mock_scaler, mock_read_csv, client):
    mock_form.validate_on_submit.return_value = False
    response = k_means_clustering()
    assert response.status_code == 200

@patch('blueprints.routes.json.load')
@patch('blueprints.routes.pickle.load')
@patch('blueprints.routes.generate_EDA')
def test_datasets(mock_json_load, mock_pickle_load, mock_generate_EDA, client):
    mock_json_load.return_value = {}
    mock_pickle_load.return_value = MagicMock()
    mock_generate_EDA.return_value = {}
    response = datasets()
    assert response.status_code == 200