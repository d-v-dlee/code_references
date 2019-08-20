import json
import pickle
from google.cloud import storage
import os
import smart_open
from gensim.models.doc2vec import Doc2Vec
import pandas as pd

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

def download_pickled_df(bucket_name, source_blob_name):
    """
    retrieves df from gcs and returns un-pickled df from gcs

    inputs
    ----
    bucket_name: name of bucket
    source_blob_name: str, path to model ex 'data/dfs/df_docs.pkl

    returns
    -----
    df
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    name = os.path.basename(source_blob_name)
    blob.download_to_filename(name)

    with open(name, 'rb') as f:
        df = pd.read_pickle(name)
    
    return df

def upload_and_pickle_df(bucket_name, destination_blob_name, df):
    """
    pickles and uploads a df to gcs

    inputs
    ----
    bucket_name: str, name of bucket
    destination_blob_name: str, path where you wanna save it
        ex data/pickled_dfs/particular_df.pkl
    df: dataframe object to pickle
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    with open('df.pkl', 'wb') as f:
        pickle.dump(df, f)
    
    blob.upload_from_filename('df.pkl')
    os.remove('df.pkl')

def download_gcs_model(bucket_name, models_dir, model_name):
    """
    Function for calling models from gcs bucket
    
    Inputs
    ------
    bucket_name: string, name of bucket
        example: 'some_bucket_name'
        
    models_dir: string, path to model zoo 
        example:  'ml-models/july-updates'
    
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

def upload_json_to_train(bucket_name, source_file, file_name):
    """
    Function for uploading json file (original + copy) into GCS bucket for retraining

    Inputs
    ------
    bucket_name: str; name of GCS bucket (ex. some_bucket_name)
    source_file: deserialized json
    file_name: str; name of file when saved to bucket appended to 'data/train/' + 'example.json'

    Outputs
    -----
    saves to gcs bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    destination_blob_name = 'data/train/' + file_name
    blob = bucket.blob(destination_blob_name)
    
    # write to a file
    with open("temp.json", "w") as f:
        json.dump(source_file, f)


    blob.upload_from_filename('temp.json') 

    print(f'File {file_name} uploaded to {destination_blob_name}.')
    return 'success'