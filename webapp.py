import os
from flask import Flask
from flask.ext import restful

import httplib
import logging
import requests
from restmarketo import Client

app = Flask(__name__)
api = restful.Api(app)

@app.route('/')
def hello():
    return 'Hello World!'

class Merge(restful.Resource):
    def post(self):
        json_input = request.get_json(force=True)
        print json_input
        return {'hello': 'world'}

api.add_resource(Merge, '/merge')

if __name__ == '__main__':
    app.run(debug=True)

    httplib.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    requests.get('http://httpbin.org/headers')

    client=Client('161-TPY-810', 'dc499150-316a-4a49-9700-19f9e2e130b3', 'r656aoxoK6WW6U1ev60KA5c6s3PemnZK')
    
    client.createUpdateLeads([{'email':'testy@testerson.org', 'firstName':'testy','lastName':'testerson'}])