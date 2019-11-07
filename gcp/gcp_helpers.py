import json
import pickle
from google.cloud import storage
import os
import smart_open
from gensim.models.doc2vec import Doc2Vec
import pandas as pd

# in order to access gcs bucket, you often need credentials
# ex: os.environ['GOOGLE_APPLICATION_CREDENTIALS']

### Working with pickled objects #####

def download_pickled_df(bucket_name, source_blob_name):
    """
    retrieves df from gcs and returns un-pickled df from gcs
    inputs
    ----
    bucket_name: name of bucket
    source_blob_name: str, path to model ex 'data/dfs/df_docs.pkl
    returns
    -----
    df: unpickled df
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    name = os.path.basename(source_blob_name)
    blob.download_to_filename(name)

    with open(name, 'rb') as f:
        df = pd.read_pickle(name)
    
    return df

def upload_and_pickle(bucket_name, destination_blob_name, object_to_pickle):
    """
    pickles and uploads a pickled object (df or model) to gcs
    inputs
    ----
    bucket_name: str, name of bucket
    destination_blob_name: str, path where you wanna save it
        ex data/pickled_dfs/particular_df.pkl
    object_to_pickle: dataframe/model object to pickle
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    with open('something.pkl', 'wb') as f:
        pickle.dump(object_to_pickle, f)
    
    blob.upload_from_filename('something.pkl')
    os.remove('something.pkl')

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

### JSON section ###

def upload_json_to_directory(bucket_name, file_to_upload, directory_name, file_name):
    """
    Function for uploading json file into a specific directory in GCP bucket.
    Inputs
    ------
    bucket_name: str; name of GCS bucket (ex. some_bucket_name)
    file_to_upload: deserialized json
<<<<<<< HEAD
    directory_name: str; name of directory in gcs bucket ex 'some_directory'
    file_name: str; name of file when saved to bucket appended to 'some_directory/' + 'example.json'
=======
    directory_name: str; name of directory in gcs bucket
    file_name: str; name of file when saved to bucket appended to 'data/train/' + 'example.json'

>>>>>>> 632da27e5dfa4e07f6adfc9fe4a18c77166cbed7
    Outputs
    -----
    saves to gcs bucket.
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    destination_blob_name = directory_name + os.sep + file_name
    blob = bucket.blob(destination_blob_name)
    
    # write to a file
    with open("temp.json", "w") as f:
        json.dump(file_to_upload, f)


    blob.upload_from_filename('temp.json') 

    print(f'File {file_name} uploaded to {destination_blob_name}.')
    return 'success'

def download_blob_as_json(bucket_name, source_blob_name):
    """
    Calls on gcs bucket and returns json as json 
    inputs
    ------
    bucket_name: name of bucket
    source_blob_name: complete path to file in bucket
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

### doc2vec section - up/downloading models ending with .model ####

def upload_doc2vec_gcs(bucket_name, destination_blob_name, d2v_model):
    """
    saves and uploads a model to gcs. different than upload_and_pickle because its saved
    as .model vs. .pkl
    inputs
    ----
    bucket_name: str, name of bucket
    destination_blob_name: str, path where you wanna save it
        ex data/pickled_dfs/particular_df.pkl
    d2v_model: doc2vec model
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    with smart_open.open('something.model', 'wb') as f:
        d2v_model.save('something.model')

    blob.upload_from_filename('something.model')
    os.remove('something.model')

def download_d2v_gcs(bucket_name, models_dir, model_name='d2v.model'):
    """
    Function for call d2v model. models_dir + model_name creates specific_model which
    is equal to source_blob_name as seen in upload.
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

################## working with blobs #################
def mv_blob(bucket_name, blob_name, new_bucket_name, new_blob_name):
    """
    Function for moving files between directories or buckets. it will use GCP's copy function then delete
    from the old directory
    
    inputs
    -----
    bucket_name: name of bucket
    blob_name: str, name of file 
        ex. 'data/some_location/file_name'
    new_bucket_name: name of bucket (can be same as original if we're just moving around directories)
    new_blob_name: str, name of file in new directory 
        ex. 'data/destination/file_name'
    """
    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.get_bucket(new_bucket_name)

    # copy to new destination
    new_blob = source_bucket.copy_blob(
        source_blob, destination_bucket, new_blob_name)
    # delete in old destination
    source_blob.delete()
    
    print(f'File moved from {source_blob} to {new_blob_name}')

def copy_blob(bucket_name, blob_name, new_bucket_name, new_blob_name):
    """
    Copies a blob from one bucket to another with a new name.
    
    Inputs
    -----
    bucket_name: str, name of bucket
    blob_name: str, name of file
    new_bucket_name: str, name of bucket - same as bucket_name if moving within directories
    new_blob_name: str, new name of file
    """
    storage_client = storage.Client()
    source_bucket = storage_client.get_bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.get_bucket(new_bucket_name)

    new_blob = source_bucket.copy_blob(
        source_blob, destination_bucket, new_blob_name)
    

def delete_blob_in_directory(bucket_name, prefix):
    """
    Function for deleting blob for directory 
    
    bucket_name: name of bucket
    prefix: prefix of filename
        ex. 'data/clean_files/some_name'
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    count = 0
    for blob in bucket.list_blobs(prefix=prefix):
        print(blob.name)
        blob.delete()
        count +=1
    print(f'{count} files starting with {prefix} removed.')