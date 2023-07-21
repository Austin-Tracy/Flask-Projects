import pytest
from wtforms import SubmitField
from ml_app.blueprints.forms import KNearestNeighborsForm, ItemSelectionForm, TimeSeriesForm, SentimentForm, KMeansClusteringForm

@pytest.fixture(params=[KNearestNeighborsForm, ItemSelectionForm, TimeSeriesForm, SentimentForm, KMeansClusteringForm])
def form_class(request):
    return request.param

def test_form_instantiation(form_class):
    form = form_class()
    assert form is not None

def test_submit_field(form_class):
    form = form_class()
    assert isinstance(form.submit, SubmitField)

def test_submit_field_label(form_class):
    form = form_class()
    assert form.submit.label.text in ['Predict Churn', 'Predict', 'Submit', 'Predict', 'Analyze Sentiment', 'Predict Cluster']

@pytest.mark.parametrize("form_class, field, default", [
    (KNearestNeighborsForm, 'Tenure', 12),
    (KNearestNeighborsForm, 'MonthlyCharge', 200),
    (KNearestNeighborsForm, 'Bandwidth_GB_Year', 1500),
    (TimeSeriesForm, 'periods', 30),
    (KMeansClusteringForm, 'TimelyResponse', 1),
    (KMeansClusteringForm, 'TimelyFix', 2),
    (KMeansClusteringForm, 'TimelyReplacement', 3),
    (KMeansClusteringForm, 'Reliability', 4),
    (KMeansClusteringForm, 'Options', 8),
    (KMeansClusteringForm, 'Respectful', 7),
    (KMeansClusteringForm, 'Courteous', 6),
    (KMeansClusteringForm, 'ActiveListening', 5),
])
def test_default_values(form_class, field, default):
    form = form_class()
    assert getattr(form, field).data == default

@pytest.mark.parametrize("form_class, field, choices", [
    (KNearestNeighborsForm, 'InternetService', [('DSL', 'DSL'), ('Fiber Optic', 'Fiber Optic'), ('None', 'None')]),
    (KNearestNeighborsForm, 'Contract', [('Month-to-month', 'Month-to-month'), ('One year', 'One year'), ('Two Year', 'Two Year')]),
    (KMeansClusteringForm, 'x_axis', [('TimelyResponse', 'TimelyResponse'), ('TimelyFix', 'TimelyFix'), ('TimelyReplacement', 'TimelyReplacement'), ('Reliability', 'Reliability'), ('Options', 'Options'), ('Respectful', 'Respectful'), ('Courteous', 'Courteous'), ('ActiveListening', 'ActiveListening')]),
    (KMeansClusteringForm, 'y_axis', [('TimelyResponse', 'TimelyResponse'), ('TimelyFix', 'TimelyFix'), ('TimelyReplacement', 'TimelyReplacement'), ('Reliability', 'Reliability'), ('Options', 'Options'), ('Respectful', 'Respectful'), ('Courteous', 'Courteous'), ('ActiveListening', 'ActiveListening')]),
])
def test_choices(form_class, field, choices):
    form = form_class()
    assert getattr(form, field).choices == choices