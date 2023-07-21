# /run.py
from pm_app import create_app
from ml_app import ml_app_blueprint
from gpt_app import gpt_blueprint

app = create_app()
app.register_blueprint(ml_app_blueprint, url_prefix='/ml_app')
app.register_blueprint(gpt_blueprint, url_prefix='/gpt')
     
if __name__ == "__main__":
    app.run()