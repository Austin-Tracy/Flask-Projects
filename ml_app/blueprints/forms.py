# ml_app/blueprints/forms.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerRangeField, BooleanField, SelectField, StringField
from wtforms.validators import DataRequired, NumberRange, InputRequired


class LinearRegressionForm(FlaskForm):
    Tenure = IntegerRangeField('Tenure', default=34, validators=[InputRequired(), NumberRange(min=0, max=71)], description='Number of years the customer has stayed with the company')
    Children = IntegerRangeField('Children', default=2, validators=[InputRequired(), NumberRange(min=0, max=10)], description='Number of children in household')
    Age = IntegerRangeField('Age', default=53, validators=[DataRequired(), NumberRange(min=18, max=89)], description='Customer age in years')
    Population = IntegerRangeField('Population', default=9756, validators=[InputRequired(), NumberRange(min=1, max=111850)], description='Estimated number of people living in city of customer')
    Income = IntegerRangeField('Income', default=39806, validators=[InputRequired(), NumberRange(min=0, max=258900)], description='Estimated yearly income of customer')
    Outage_sec_perweek = IntegerRangeField('Outage_sec_perweek', default=10, validators=[InputRequired(), NumberRange(min=0, max=21)], description='Estimated outage in seconds per week')
    Email = IntegerRangeField('Email', default=12, validators=[InputRequired(), NumberRange(min=0, max=23)], description='Number of email exchanges with this customer')
    Contacts = IntegerRangeField('Contacts', default=1, validators=[InputRequired(), NumberRange(min=0, max=7)], description='Number of contacts customer has')
    Yearly_equip_failure = IntegerRangeField('Yearly_equip_failure', default=1, validators=[InputRequired(), NumberRange(min=0, max=6)], description='Number of equipment failures in past year')
    Bandwidth_GB_Year = IntegerRangeField('Bandwidth_GB_Year', default=3392, validators=[InputRequired(), NumberRange(min=155, max=7158)], description='Estimated bandwidth used in GB/year')
    submit = SubmitField('Predict Monthly Charge')

class LogisticRegressionForm(FlaskForm):
    Children = IntegerRangeField('Children', default=2, validators=[InputRequired(), NumberRange(min=0, max=10)], description='Number of children in household')
    Age = IntegerRangeField('Age', default=53, validators=[DataRequired(), NumberRange(min=18, max=89)], description='Age of customer in years')
    Contacts = IntegerRangeField('Contacts', default=1, validators=[InputRequired(), NumberRange(min=0, max=7)], description='Number of contacts with customer service')
    Yearly_equip_failure = IntegerRangeField('Yearly_equip_failure', default=1, validators=[InputRequired(), NumberRange(min=0, max=6)], description='Number of equipment failures in past year')
    Techie = BooleanField('Techie', description='Customer is technically inclined', default=True)
    Port_modem = BooleanField('Port_modem', description='Customer has portable modem add-on')
    Tablet = BooleanField('Tablet', description='Customer has tablet add-on')
    Multiple = BooleanField('Multiple', description='Customer has multiple lines')
    OnlineSecurity = BooleanField('OnlineSecurity', description='Customer has online security add-on')
    OnlineBackup = BooleanField('OnlineBackup', description='Customer has online backup add-on')
    DeviceProtection = BooleanField('DeviceProtection', description='Customer has device protection add-on')
    TechSupport = BooleanField('TechSupport', description='Customer has tech support add-on')
    StreamingTV = BooleanField('StreamingTV', description='Customer has streaming TV add-on', default=True)
    StreamingMovies = BooleanField('StreamingMovies', description='Customer has streaming movies add-on', default=True)
    PaperlessBilling = BooleanField('PaperlessBilling', description='Customer has paperless billing')
    PaymentMethod = SelectField('PaymentMethod', choices=[
        ('PaymentMethod_Bank Transfer(automatic)', 'Bank Transfer (automatic)'), 
        ('PaymentMethod_Credit Card (automatic)', 'Credit Card (automatic)'),
        ('PaymentMethod_Electronic Check', 'Electronic Check'), 
        ('PaymentMethod_Mailed Check', 'Mailed Check')], description='Customer payment method')
    # Add the rest of the fields here...
    submit = SubmitField('Predict Churn')

class KNearestNeighborsForm(FlaskForm):
    Techie = BooleanField('Techie', description='Customer is technically inclined')
    Multiple = BooleanField('Multiple', description='Customer has multiple lines')
    OnlineBackup = BooleanField('OnlineBackup', description='Customer has online backup add-on')
    DeviceProtection = BooleanField('DeviceProtection', description='Customer has device protection add-on')
    StreamingTV = BooleanField('StreamingTV', description='Customer has streaming TV add-on')
    StreamingMovies = BooleanField('StreamingMovies', description='Customer has streaming movies add-on')
    Tenure = IntegerRangeField('Tenure', default=12, validators=[InputRequired(), NumberRange(min=0, max=71)], description='Number of years the customer has stayed with the company')
    MonthlyCharge = IntegerRangeField('MonthlyCharge', default=200, validators=[InputRequired(), NumberRange(min=79, max=290)], description='Monthly charge')
    Bandwidth_GB_Year = IntegerRangeField('Bandwidth_GB_Year', default=1500, validators=[InputRequired(), NumberRange(min=155, max=7158)], description='Estimated bandwidth used in GB/year')
    InternetService = SelectField('InternetService', choices=[
        ('DSL', 'DSL'), 
        ('Fiber Optic', 'Fiber Optic'), 
        ('None', 'None')], description='Customer internet service type')
    Contract = SelectField('Contract', choices=[
        ('Month-to-month', 'Month-to-month'), 
        ('One year', 'One year'), 
        ('Two Year', 'Two Year')], description='Customer contract type')
    submit = SubmitField('Predict')

class ItemSelectionForm(FlaskForm):
    item = SelectField('Item', choices=[], description='Possible product options to show recommendations') # choices will be populated dynamically
    submit = SubmitField('Submit')

class TimeSeriesForm(FlaskForm):
    periods = IntegerRangeField('Days into the future', default=30, validators=[InputRequired(), NumberRange(min=1, max=365)], description='Number of days into the future to predict')
    submit = SubmitField('Predict')

class SentimentForm(FlaskForm):
    text = StringField('Text', validators=[InputRequired()], description='Text to analyze')
    submit = SubmitField('Analyze Sentiment')

class KMeansClusteringForm(FlaskForm):
    TimelyResponse = IntegerRangeField('TimelyResponse', default=1, validators=[InputRequired(), NumberRange(min=1, max=8)], description='Survey response in regards to timely responses')
    TimelyFix = IntegerRangeField('TimelyFix', default=2, validators=[InputRequired(), NumberRange(min=1, max=8)], description='Survey response in regards to timely fixes')
    TimelyReplacement = IntegerRangeField('TimelyReplacement', default=3, validators=[DataRequired(), NumberRange(min=1, max=8)], description='Survey response in regards to timely replacements')
    Reliability = IntegerRangeField('Reliability', default=4, validators=[InputRequired(), NumberRange(min=1, max=8)], description='Survey response in regards to service reliability')
    Options = IntegerRangeField('Options', default=8, validators=[InputRequired(), NumberRange(min=1, max=8)], description='Survey response in regards to available options')
    Respectful = IntegerRangeField('Respectful', default=7, validators=[InputRequired(), NumberRange(min=1, max=8)], description='Survey response in regards to respectful customer service')
    Courteous = IntegerRangeField('Courteous', default=6, validators=[InputRequired(), NumberRange(min=1, max=8)], description='Survey response in regards to courteous customer service')
    ActiveListening = IntegerRangeField('ActiveListening', default=5, validators=[InputRequired(), NumberRange(min=1, max=8)], description='Survey response in regards to active listening')
    x_axis = SelectField('X Axis', choices=[
        ('TimelyResponse', 'TimelyResponse'), 
        ('TimelyFix', 'TimelyFix'),
        ('TimelyReplacement', 'TimelyReplacement'),
        ('Reliability', 'Reliability'),
        ('Options', 'Options'),
        ('Respectful', 'Respectful'),
        ('Courteous', 'Courteous'),
        ('ActiveListening', 'ActiveListening')
    ], description='Survey Feature to plot on the x-axis')
    y_axis = SelectField('Y Axis', choices=[
        ('TimelyResponse', 'TimelyResponse'), 
        ('TimelyFix', 'TimelyFix'),
        ('TimelyReplacement', 'TimelyReplacement'),
        ('Reliability', 'Reliability'),
        ('Options', 'Options'),
        ('Respectful', 'Respectful'),
        ('Courteous', 'Courteous'),
        ('ActiveListening', 'ActiveListening')
    ], description='Survey Feature to plot on the y-axis')
    submit = SubmitField('Predict Cluster')