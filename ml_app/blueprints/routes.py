# ml_app/blueprints/routes.py
import pickle
import os
import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objs as go
from flask import render_template, request, flash, redirect, url_for, session, Response, current_app
from ml_app import ml_app_blueprint as ml_app
from ml_app.blueprints.forms import LinearRegressionForm, LogisticRegressionForm, KNearestNeighborsForm, ItemSelectionForm, TimeSeriesForm, SentimentForm, KMeansClusteringForm
from ml_app.models.frequent_itemsets import get_product_rules
from ml_app.models.sentiment_analysis import predict_sentiment
from ml_app.models.kmeans import KMeans
from ml_app.models.custom_scaler import CustomScaler
from ml_app.models.eda import generate_EDA
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

routes = [
        {'name': 'Home', 'url': 'ml_app_home'},
        {'name': 'Logistic Regression', 'url': 'logistic_regression'},
        {'name': 'Linear Regression', 'url': 'linear_regression'},
        {'name': 'K-Nearest Neighbors', 'url': 'k_nearest_neighbors'},
        {'name': 'Frequent Itemsets', 'url': 'frequent_itemsets'},
        {'name': 'Time Series', 'url': 'time_series'},
        {'name': 'Sentiment Analysis', 'url': 'sentiment_analysis'},
        {'name': 'K-Means Clustering', 'url': 'k_means_clustering'},
        {'name': 'Datasets', 'url': 'datasets'},
    ]

@ml_app.route('/')
def ml_app_home() -> Response:
    return render_template('ml_app_home.html')


@ml_app.route('/logistic_regression', methods=['GET', 'POST'])
def logistic_regression() -> Response:
    """
    Renders the logistic regression page and handles form submission to make predictions using a trained logistic regression model.

    Returns:
        rendered HTML template: The logistic regression page with a form to input feature values and display the predicted value.
    """
    form = LogisticRegressionForm()

    # Load the logistic regression model
    with open(os.path.join('ml_app', 'trained_models', 'logistic_regression.pkl'), 'rb') as f:
        churn_model = pickle.load(f)

    prediction = None
    feature_order = ['Children', 'Age', 'Contacts', 'Yearly_equip_failure', 'Techie', 'Port_modem',
                     'Tablet', 'Multiple', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                     'TechSupport', 'StreamingTV', 'StreamingMovies', 'PaperlessBilling',
                     'PaymentMethod_Bank Transfer(automatic)',
                     'PaymentMethod_Credit Card (automatic)', 'PaymentMethod_Electronic Check',
                     'PaymentMethod_Mailed Check']

    if form.validate_on_submit():
        input_data = form.data
        payment_method = input_data.get('PaymentMethod')

        # Prepare data dictionary
        input_data = {
            **input_data,
            **{f'PaymentMethod_{method}': int(method == payment_method) for method in ['Bank Transfer(automatic)', 'Credit Card (automatic)', 'Electronic Check', 'Mailed Check']}
        }
        input_data.pop('PaymentMethod', None)
        input_data.pop('submit', None)
        input_data.pop('csrf_token', None)

        # Reorder the input_data according to the feature_order
        input_data = {k: input_data[k] for k in feature_order}

        try:
            churn_prediction = churn_model.predict(pd.DataFrame([input_data]))
            prediction_proba = churn_model.predict_proba(pd.DataFrame([input_data]))
            churn_probability = prediction_proba[0][1] * 100  # Get the probability of class 'churned'
            prediction = {
                'text': "Customer will Churn",
                'probability': round(churn_probability, 2)
            }
            if prediction['probability'] > 99:
                prediction['probability'] = 99
        except Exception as e:
            print(f'Error making prediction: {e}')

    return render_template('logistic_regression.html', model=churn_model, prediction=prediction, form=form)


# Define route for linear regression page
@ml_app.route('/linear_regression', methods=['GET', 'POST'])
def linear_regression() -> Response:
    """
    Renders the linear regression page and handles form submission to make predictions using a trained linear regression model.

    Returns:
        rendered HTML template: The linear regression page with a form to input feature values and display the predicted value.
    """
    # Create a form object
    form = LinearRegressionForm()
    prediction = None
    if request.method == 'POST':
        if form.validate_on_submit() == False:
            flash('All form fields are required.')
            return redirect(url_for('ml_app.linear_regression'))
        if form.validate_on_submit():
            # Load the linear regression model
            linear_regression_model = pickle.load(open(os.path.join('ml_app', 'trained_models', 'linear_regression.pkl'), 'rb'))
            # Prepare the input features
            input_features = [[
                form.Population.data,
                form.Children.data,
                form.Age.data,
                form.Income.data,
                form.Outage_sec_perweek.data,
                form.Email.data,
                form.Contacts.data,
                form.Yearly_equip_failure.data,
                form.Tenure.data,
                form.Bandwidth_GB_Year.data
            ]]
            prediction = linear_regression_model.predict(input_features)[0]
            if not prediction:
                flash('Error: prediction failed.')
                print('Error: prediction failed.')
                return redirect(url_for('ml_app.linear_regression'))
            prediction = round(prediction, 2)
            print(prediction)
    return render_template('linear_regression.html', form=form, prediction=prediction)

@ml_app.route('/k_nearest_neighbors', methods=['GET', 'POST'])
def k_nearest_neighbors() -> Response:
    """
    This function defines the route for the k-nearest neighbors page. It renders the k_nearest_neighbors.html template and 
    handles the form submission. It retrieves the trained k-nearest neighbors model from the 'knn_model.pkl' file and uses it 
    to make a prediction based on the user's input. The form data is preprocessed to match the format expected by the model, 
    and the prediction is returned as a dictionary containing the predicted class and the probability of the prediction. 
    The function then renders the k_nearest_neighbors.html template with the form and the prediction.

    Returns:
        The rendered template for the k-nearest neighbors page.
    """
    form = KNearestNeighborsForm()
    prediction = None
    feature_order = ['Techie', 'Multiple', 'OnlineBackup', 'DeviceProtection', 'StreamingTV',
                     'StreamingMovies', 'Tenure', 'MonthlyCharge', 'Bandwidth_GB_Year',
                     'InternetService_DSL', 'InternetService_Fiber Optic',
                     'InternetService_None', 'Contract_Month-to-month', 'Contract_One year',
                     'Contract_Two Year']

    if form.validate_on_submit():
        form_data = form.data
        internet_service = form_data.get('InternetService')
        contract = form_data.get('Contract')

        # Prepare data dictionary
        form_data = {
            **form_data,
            **{f'InternetService_{value}': int(value == internet_service) for value in ['DSL', 'Fiber Optic', 'None']},
            **{f'Contract_{value}': int(value == contract) for value in ['Month-to-month', 'One year', 'Two Year']}
        }
        form_data.pop('InternetService', None)
        form_data.pop('Contract', None)
        form_data.pop('submit', None)
        form_data.pop('csrf_token', None)

        # Reorder the form_data according to the feature_order
        form_data = {k: form_data[k] for k in feature_order}

        try:
            knn_model = pickle.load(open(os.path.join('ml_app', 'trained_models', 'knn_model.pkl'), 'rb'))
            churn_prediction = knn_model.predict(pd.DataFrame(np.array([list(form_data.values())]), columns=list(form_data.keys())).replace({True: 1, False: 0}))
            prediction_proba = knn_model.predict_proba(pd.DataFrame(np.array([list(form_data.values())]), columns=list(form_data.keys())).replace({True: 1, False: 0}))
            churn_probability = prediction_proba[0][1] * 100  # Get the probability of class 'churned'
            prediction = {
                'text': "Customer will Churn",
                'probability': round(churn_probability, 2)
            }
            if prediction['probability'] > 99:
                prediction['probability'] = 99
        except Exception as e:
            print(f'Error making prediction: {e}')

    return render_template('k_nearest_neighbors.html', form=form, prediction=prediction)



@ml_app.route('/frequent_itemsets', methods=['GET', 'POST'])
def frequent_itemsets() -> Response:
    """
    This function defines the route for the frequent itemsets page. It renders the frequent_itemsets.html template and 
    handles the form submission. It retrieves the product rules and product list from the get_product_rules() function and 
    dynamically populates the item selection form with the product list. When the form is submitted, it retrieves the 
    selected item and uses it to filter the product rules to get the top 3 recommended items. It then renders the 
    frequent_itemsets.html template with the form and the recommendations.

    Returns:
        The rendered template for the frequent itemsets page.
    """
    product_rules, product_list = get_product_rules()
    form = ItemSelectionForm()
    form.item.choices = [(item, item) for item in product_list] # dynamic choices
    recommendations = set()
    if form.validate_on_submit():
        selected_item = form.item.data
        mask = product_rules['antecedents'].apply(lambda x: selected_item in str(x))
        raw_recommendations = product_rules[mask].sort_values(by='confidence', ascending=False)['consequents'].tolist()
        # Convert frozensets into strings and add to the set
        for r in raw_recommendations:
            item = list(r)[0]
            if item != 'Dust-Off Compressed Gas 2 pack':
                recommendations.add(item)
                if len(recommendations) >= 3:  # stop when we have 3 unique recommendations
                    break
    return render_template('frequent_itemsets.html', form=form, recommendations=list(recommendations))


@ml_app.route('/sentiment_analysis', methods=['GET', 'POST'])
def sentiment_analysis() -> Response:
    """
    This function defines the route for the sentiment analysis page. It renders the sentiment_analysis.html template and 
    handles the form submission. It predicts the sentiment of the text entered in the form using the predict_sentiment() 
    function and displays the predicted sentiment. It also stores the text and predicted sentiment in the session data 
    and displays the history of text and predicted sentiment. 

    Returns:
        The rendered template for the sentiment analysis page.
    """
    # Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
    # Sentiment Analysis of Social Media Text. Eighth International Conference on
    # Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
    form = SentimentForm()
    sentiment = None

    if request.method == 'GET':
        session.pop('sentiment_history', None)  # Clear the session data if request is GET
        sentiment_history = []
    else:
        sentiment_history = session.get('sentiment_history', [])  # Get the session data if exists
    
    if form.validate_on_submit():
        
        sentiment = predict_sentiment(form.text.data)
        flash(f'Predicted Sentiment: {sentiment}')
        sentiment_history.append({'text': form.text.data, 'sentiment': sentiment})
        session['sentiment_history'] = sentiment_history  # Store back in the session

    return render_template('sentiment_analysis.html', form=form, sentiment=sentiment, sentiment_history=sentiment_history)



# Define route for time series page
@ml_app.route('/time_series', methods=['GET', 'POST'])
def time_series() -> Response:
    """
    Renders the time series page and generates a forecast using an ARIMA model.

    Returns:
        The rendered time series page with a forecast plot and form for user input.
    """
    # Create a form object
    form = TimeSeriesForm()

    # Load the time series data
    data = pd.read_csv(os.path.join('ml_app', 'data', 'cleaned_time_series.csv'))
    data.index = pd.to_datetime(data.index)

    # Initialize variables
    forecast = None
    traces = None

    # Get the forecast history from the session data
    if request.method == 'GET':
        session.pop('forecast_history', None)  # Clear the session data if request is GET
        forecast_history = []
    else:
        forecast_history = session.get('forecast_history', [])  # Get the session data if exists

    # Generate the forecast if the form is submitted
    if form.validate_on_submit():
        # Load the ARIMA model
        with open(os.path.join('ml_app', 'trained_models', 'stepwise_arima.pkl'), 'rb') as pkl:
            arima_model = pickle.load(pkl)

        # Generate the forecast
        forecast = arima_model.predict(n_periods=form.periods.data)

        # Set up the forecast dataframe
        today = datetime.now()
        start_date = today - timedelta(days=len(data))
        forecast = pd.DataFrame(forecast, index=pd.date_range(start=today, periods=form.periods.data, freq='D'))

        # Set up the traces for the plot
        traces = []
        for column in forecast.columns:
            traces.append(go.Scatter(x = forecast.index, y = forecast[column], mode = 'lines', name = column))

        # Convert the traces to JSON for rendering in the template
        traces_json = json.dumps(traces, cls=plotly.utils.PlotlyJSONEncoder)

        # Add the forecast to the session history
        forecast_history.append({'days': form.periods.data, 'forecast': forecast.iloc[-1, 0]})
        session['forecast_history'] = forecast_history  # Store back in the session

        # Render the template with the forecast plot and form
        return render_template('time_series.html', form=form, traces=traces_json, forecast=forecast, forecast_history=forecast_history)

    # Render the template with the form only
    else:
        return render_template('time_series.html', form=form, forecast=forecast, traces=traces, forecast_history=forecast_history)


@ml_app.route("/k_means_clustering", methods=['GET', 'POST'])
def k_means_clustering() -> Response:
    """
    Renders the K-Means Clustering page and handles form submission. Loads the KMeans model and Scaler from text files,
    standardizes the form data, predicts the cluster for the form data, and creates scatter plot data for each cluster.

    Returns:
        Rendered HTML template with the K-Means Clustering page, form data, predicted cluster, and scatter plot data.
    """
    form = KMeansClusteringForm()
    plot_data = None
    user_cluster = None
    user_label = None
    x_axis = None
    y_axis = None
    if form.validate_on_submit():
        x_axis = form.x_axis.data
        y_axis = form.y_axis.data

        # Load the KMeans model (centroids) from a text file named 'centroids.txt'
        centroids = np.loadtxt(os.path.join('ml_app', 'trained_models', 'centroids.txt'))

        # Create a new KMeans instance and load the centroids
        kmeans = KMeans(K=4, max_iters=100, plot_steps=False)
        kmeans.load_centroids(centroids)

        scaler = CustomScaler()
        # Load the Scaler from a text file named 'scaler.txt'
        scaler.means = np.loadtxt(os.path.join('ml_app', 'trained_models', 'scaler_means.txt'))
        scaler.stds = np.loadtxt(os.path.join('ml_app', 'trained_models', 'scaler_stds.txt'))

        # Get the data from the form
        form_data = np.array([form.TimelyResponse.data, form.TimelyFix.data, form.TimelyReplacement.data,
                              form.Reliability.data, form.Options.data, form.Respectful.data,
                              form.Courteous.data, form.ActiveListening.data]).reshape(1, -1)

        # Standardize the form data
        standardized_data = scaler.transform(form_data)

        # Predict the cluster
        user_cluster = int(kmeans.predict(standardized_data)[0])

        survey_columns = ["TimelyResponse", "TimelyFix", "TimelyReplacement",
                            "Reliability", "Options", "Respectful", "Courteous",
                            "ActiveListening"]

        # Load the full dataset
        X = pd.read_csv(os.path.join('ml_app', 'data', 'churn_clean.csv'))

        X = X[survey_columns]

        # Only select numeric columns
        X = pd.DataFrame(scaler.transform(X), columns=survey_columns)  # Apply the same scaler used on form data

        # Get the cluster labels for all data
        labels = kmeans.predict(X.to_numpy())

        cluster_labels = ['Good', 'Very Poor', 'Very Good', 'Poor']

        # Create scatter plot data for each cluster
        plot_data = []
        for i, centroid in enumerate(centroids):
            cluster_data = X[labels == i]
            label = cluster_labels[i]
            print(cluster_data)
            cluster_dict = {
                'x': cluster_data[x_axis].tolist(),
                'y': cluster_data[y_axis].tolist(),
                'mode': 'markers',
                'type': 'scatter',
                'name': label,
                'hovertemplate':
                    '<i>{}</i>: %{{x}}'.format(x_axis) +
                    '<br><b>{}</b>: %{{y}}<br>'.format(y_axis)
            }

            if i == user_cluster:
                cluster_dict['marker'] = {'symbol': 'x', 'size': 9, 'opacity': 1.0}  # highlight user's cluster
                user_label = label

            plot_data.append(cluster_dict)
    return render_template("k_means_clustering.html", form=form, cluster=user_cluster, label=user_label, plot_data=plot_data, routes=routes, x_axis=x_axis, y_axis=y_axis)


@ml_app.route('/datasets', methods=['GET'])
def datasets() -> Response:
    """
    This function loads a dataset and its headers, filters the columns, and generates an exploratory data analysis (EDA) HTML
    report for the dataset. The EDA report is generated using the generate_EDA function from the utils.generate_timeline module.
    The function returns a rendered HTML template with the filtered dataset, headers, feature descriptions, target variable, and
    EDA report.
    """
    # Load feature descriptions
    with open('ml_app/static/files/features.json') as json_file:
        feature_descriptions = json.load(json_file)

    # Load the dataset and headers
    with open('ml_app/data/churn_clean.pkl', 'rb') as f:
        dataset = pickle.load(f)

    headers = dataset.columns
    data = dataset.values

    feature_vars = ['Population', 'Area', 'Children', 'Age', 'Income', 'Marital', 'Gender',
       'Outage_sec_perweek', 'Email', 'Contacts', 'Yearly_equip_failure',
       'Techie', 'Contract', 'Port_modem', 'Tablet', 'InternetService',
       'Phone', 'Multiple', 'OnlineSecurity', 'OnlineBackup',
       'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
       'PaperlessBilling', 'PaymentMethod', 'Tenure', 'MonthlyCharge',
       'Bandwidth_GB_Year', 'TimelyResponse', 'TimelyFix', 'TimelyReplacement',
       'Reliability', 'Options', 'Respectful', 'Courteous', 'ActiveListening']

    # convert numpy array to dataframe with original headers
    df = pd.DataFrame(data, columns=headers)

    # filter dataframe columns
    df = df[feature_vars + ['Churn']]

    # convert dataframe back to numpy array
    # only the first 100 rows
    data = df.values[:100]

    # filter headers
    headers = [header for header in headers if header in feature_vars]

    target_var = "Churn"

    eda_html_dict = generate_EDA(df, feature_vars, target_var)
    print(feature_descriptions)
    return render_template('datasets.html',
                           data=data,
                           headers=headers,
                           feature_descriptions=feature_descriptions,
                           feature_vars=feature_vars,
                           target_var=target_var,
                           eda_html_dict=eda_html_dict)