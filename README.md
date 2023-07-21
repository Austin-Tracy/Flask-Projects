# Flask Application Overview
This repository consists of three major projects: Study Application (gpt_app), Project Management App (pm_app), and a Machine Learning Flask Web Application (ml_app). Each application is developed using Flask and serves a unique purpose. Below is a brief overview of each project. Detailed information about each application is available in their respective folders.

## Table of Contents
- [Study Application](#study-application)
- [Project Management App](#project-management-app)
- [Machine Learning Flask Web Application](#machine-learning-flask-web-application)
- [License](#license)

## Study Application
The Study Application is designed to manage and create interactive study conversations. The application can create, retrieve, and manage conversations, and generate study questions for a given conversation. It also allows the user to interact with a GPT chatbot and generate study questions from the interaction. Visit the [Study Application directory](/gpt_app/) for more details.

## Project Management App
pm_app is a Flask-based web application that provides a platform for efficient project and task management. The application is equipped with user authentication, project management, task management, task history, user activity tracking, and user profile management features. Detailed documentation is available in the [Project Management directory](/pm_app/).

## Machine Learning Flask Web Application
The Machine Learning Flask Web Application provides a user-friendly interface to a diverse selection of machine learning models. By entering data into various forms, users can receive insightful predictions based on their unique inputs. It includes models like Logistic Regression, Linear Regression, K-Nearest Neighbors, Frequent Itemsets, Sentiment Analysis, Time Series Analysis, and K-Means Clustering. For more details, visit the [Machine Learning directory](/ml_app/).

## Usage
*Update your DATABASE_URL, OPENAI_API_KEY, AND OPENAI_ORG keys in the "envtemplate" file.
Be sure to rename the "envtemplate" file to ".env"  and confirm ".env" has been added to your ".gitignore" file.*

To run any of the applications, clone the repository and install the dependencies using the following commands:
```bash
git clone
cd <application_directory>
pip install -r requirements.txt
```
Then, run the application using the following command:
```bash
flask run
```
The application will be available at `http://localhost:5000/`.


## License
All the projects in this repository are licensed under the terms of the MIT license.