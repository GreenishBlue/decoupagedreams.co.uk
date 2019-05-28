# Decoupage Dreams webapp
To access the private staging environment at https://decoupage-dreams.appspot.com, 
you must be whitelisted to get access.

## Dependencies
* Node.js/NPM
* Python 3.7
* Google Cloud SDK (for deployment only)
* Use `pip install -r requirements.txt` to install Python deps

## Debugging
Make sure Node.js/NPM/Python 3 and dependencies are up-to-date. 

`export FLASK_DEBUG=1; export FLASK_APP=main.py`
Run `npm start` and `flask run` simultaneously. 

## Building

`npm run-script build`

## Deploying
First build the program, and then use `gcloud` to deploy to App Engine

`gcloud app deploy`

## Continuous integration with Cloud Build
Make sure to [read the following guide](https://cloud.google.com/source-repositories/docs/quickstart-triggering-builds-with-source-repositories) on setting up Cloud Build's service account to have App Engine admin permissions.
