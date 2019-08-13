import os
import falcon
import pdb

# health check
service_is_healthy = True
try:
    # check for correct passed env variables
    credentials_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    bucket_name = os.environ['BUCKET']
    models_dir = 'ml-models' + os.sep + os.environ['MODELS']
except:
    service_is_healthy = False


def process(source_transcript_json):
    """
    Accepts source_transcript_json and json_str_name and outputs 
    """
    # pdb.set_trace() # test
    output_json = infer(bucket_name, source_transcript_json, models_dir) 
    success = upload_json_to_train(bucket_name, output_json, output_json['transcript_name'])
    return output_json
    

class suggestionHandler(object):

    def on_post(self, req, resp):
        if service_is_healthy:
            processed_json = process(req.media)
            if processed_json:
                resp.media = processed_json
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_500
        else:
            resp.status = falcon.HTTP_500


class trainingHandler(object):

    def on_post(self, req, resp):
        # resp.status = falcon.HTTP_501  # Not implemented

        if service_is_healthy:
            success = upload_json_to_train(bucket_name, req.media, req.media['transcript_name'])
            if success:
                resp.media = {'status': 'uploaded for training'}
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_500
        else:
            resp.status = falcon.HTTP_500


class healthCheck(object):

    def on_get(self, req, resp):
        # Note: more involved health checking can be done here if desired.
        if service_is_healthy:
            resp.media = {"health": "ok"}
            resp.status = falcon.HTTP_200
        else:
            pdb.set_trace()
            resp.status = falcon.HTTP_500

