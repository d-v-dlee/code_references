import falcon
from falcon_functions import suggestionHandler, trainingHandler, healthCheck

api = application = falcon.API()

suggestions = suggestionHandler()
api.add_route('/suggestion', suggestions)

training = trainingHandler()
api.add_route('/training', training)

health_check = healthCheck()
api.add_route('/healthy', health_check)