from flask import Flask
from flask_restful import Resource, Api
from flask import request

from hashids import Hashids

import random

from urllib.parse import urlparse

hashids = Hashids()

app = Flask(__name__)
api = Api(app)
appUrl = "http://localhost:5000/url/"

urls = []
count = 0

class Url(Resource):
    def get(self, url_hash):
        retVal = {}
        url = globals()['urls']
        if len(url) > 0:
            for i in range(0, len(url)):
                parsed_obj = urlparse(url[i]['short'])
                hashVal = parsed_obj.path
                k, m,hashv = hashVal.split('/')
                if hashv == url_hash:
                    retVal['id'] = url[i]['id']
                    retVal['short'] = url[i]['short']
                    retVal['url'] = url[i]['long']
                    retCode = 200
                else:
                    retCode = 404
        else:
            retCode = 404
        return retVal, retCode

    def delete(self, url_hash):
        url = globals()['urls']
        if len(url) > 0:
            for i in range(0, len(url)):
                parsed_obj = urlparse(url[i]['short'])
                hashVal = parsed_obj.path
                k, m, hashv = hashVal.split('/')
                if hashv == url_hash:
                    (globals()['urls'].clear())
                    retCode = 204
                else:
                    retCode = 404
        else:
            retCode = 404
        return {}, retCode

class ShortenUrl(Resource):
    def post(self):
        globals()['count'] += 1
        url = globals()['urls']
        addVal = {}
        hashids = globals()['hashids']
        updatedurl = request.get_data().decode('utf-8')
        key, value = updatedurl.split('=')
        if len(url) > 0:
            for i in range(0,len(url)):
                if value == url[i]['long']:
                    return {}, 409
        hashVal = hashids.encrypt(random.randint(100,999))
        shortUrl = appUrl + hashVal
        addVal['id'] = globals()['count']
        addVal['short'] = shortUrl
        addVal['long'] = value
        url.append(addVal)
        return addVal, 201

api.add_resource(ShortenUrl, '/url')
api.add_resource(Url, '/url/<string:url_hash>')

if __name__ == '__main__':
    app.run(debug=True)