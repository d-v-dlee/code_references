import json
import pickle
from google.cloud import storage
import os
import smart_open
from gensim.models.doc2vec import Doc2Vec

# in order to access gcs bucket, you often need credentials
# ex: os.environ['GOOGLE_APPLICATION_CREDENTIALS']

def download_blob_as_json(bucket_name, source_blob_name):
    """
    Calls on gcs bucket and returns json as json 

    inputs
    ------
    bucket_name: name of bucket
    source_blob_name: path to file
        example: 'data/inference/transcript-copy-2640899533-1295116867788-e7e32108913abd1f.json'

    returns
    -----
    json_data: dict of data
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    j = blob.download_as_string()
    json_data = json.loads(j.decode('utf-8'))
    
    return json_data

def download_gcs_model(bucket_name, models_dir, model_name):
    """
    Function for calling models from gcs bucket
    
    Inputs
    ------
    bucket_name: string, name of bucket
        example: 'transcriptions-modalis-dev-crackling'
        
    models_dir: string, path to model zoo 
        example:  'ml-models/model-zoo-2019-07-25'
    
    model_name: string, name of model
        example: context_only_model.pkl
    
    Returns
    -------
    model: unpickled model
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    
    # get name of model
    specific_model = models_dir + os.sep + model_name

    blob = bucket.blob(specific_model)
    
    # create file
    filename = os.path.basename(specific_model)
    blob.download_to_filename(filename)
    
    # unpickle model
    with open(filename, 'rb') as f:
        model = pickle.load(f)

    return model

def download_d2v_gcs(bucket_name, models_dir, model_name='d2v.model'):
    """
    Function for call d2v model

    inputs
    -------
    bucket_name: string, name of bucket NOT project
    models_dir: string, path of directory to model NOT including model name
    model_name: name of model

    returns
    -----
    d2vmodel
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    # get name of model
    specific_model = models_dir + os.sep + model_name

    blob = bucket.blob(specific_model)
    
    filename = os.path.basename(specific_model)
    blob.download_to_filename(filename)
    
    with smart_open.open(filename, 'rb') as f:
        d2v_model = Doc2Vec.load(filename)
    
    return d2v_model