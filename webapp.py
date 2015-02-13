import os
from flask import Flask, request
from flask.ext import restful

import httplib
import logging
import requests
from restmarketo import Client

app = Flask(__name__)
api = restful.Api(app)

# logging
httplib.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
requests.get('http://httpbin.org/headers')

# just a route
@app.route('/')
def hello():
    return 'Hello World!'

# this is the main part of the app - this is a rest api.  the webhook from marketo hits this script.
class Merge(restful.Resource):
    def post(self):
        json_input = request.get_json(force=True)
        #for local testing only
        #email = json_input['email']
        email = str(json_input)
        client = Client('123-3GY-831','f0ff32b61-9545-4c43-b1f5-c2c1623f361f','YQ2hi3qs4dfrJRdf439LUQss9lx3VMU')
        leads = client.getMultipleLeadsByFilterType('email', [email], fields=['email','firstName'])
        # find the lead that should be the winner
        winningLeadId = str(leads[1]['id'])
        losingLeadId = str(leads[0]['id'])
        client.mergeLeads(winningLeadId, losingLeadId)
        return leads

'''
# this may not be necessary since we only have 2 leads in this use case.
def determineWinningLead(leads):
    # Takes in a json array of leads and returns the winning lead
    # based on the one that is last created, which will be the SFDC one
    # initialize a winning lead
    winningLead = leads[0]
    for lead in leads:
        if winningLead['id'] < lead['id']:
            winningLead = lead
    return winningLead
'''
api.add_resource(Merge, '/merge')

if __name__ == '__main__':
    app.run(debug=True)
    print 'app loaded'
