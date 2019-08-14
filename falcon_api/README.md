## This directory is a reference for building an API using Falcon. 
#### app.py
app.py is the script you would be running to for an API. This could be done through Docker, or you could run it using guniorn on server
(in addition to screen or other application that keeps script running on server). 
#### falcon_functions.py
falcon_functions.py contains the code needed to run app.py. in addition to this script, you could have additional helper files. in the example in this directory, it is looking for environment variables to run.

### example
gunicorn --reload app \
-e GOOGLE_APPLICATION_CREDENTIALS = goog_creds.json \
-e BUCKEY = some_bucket \
-e MODELS = models_folder \
--timeout = 600
