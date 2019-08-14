## This directory is a reference for building an API using Falcon. 
#### app.py
app.py is the script you would be running to for an API. This could be done through Docker, or you could run it using guniorn on server
(in addition to screen or other application that keeps script running on server). 
#### falcon_functions.py
falcon_functions.py contains the code needed to run app.py. in addition to this script, you could have additional helper files. in the example in this directory, it is looking for environment variables to run.

an important function run in falcon_functions.py is `process` which runs the function `infer`. in reality, `infer` would be being imported from another script you wrote. `infer` is a function that runs through a pipeline of ML models and then returns and trandformed json.

`process` and therefore `infer` are run whwn the `/suggestion/` part of the API is run.

### example
gunicorn --reload app \
-e GOOGLE_APPLICATION_CREDENTIALS = goog_creds.json \
-e BUCKEY = some_bucket \
-e MODELS = models_folder \
--timeout = 600
