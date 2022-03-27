import requests
import time

class TwitterClient():
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def __init__(self, token):
        super().__init__()
        self.endpoint = 'https://api.twitter.com/2/tweets/'
        self.headers = {"Authorization": token}

    def request(self, request_type, query, parameters):
        endpoint = self.endpoint

        if request_type == 'search':
            endpoint += 'search/all?query='+query
        elif request_type == 'count':
            endpoint += 'counts/all?query='+query

        for parameter in parameters:
            endpoint += '&' + parameter + '='
            if type(parameters[parameter]) == list:
                endpoint +=  ",".join(parameters[parameter])
            else:
                endpoint += parameters[parameter]

        r = requests.get(endpoint, headers=self.headers).json()
        
        if request_type == 'count':
            if 'next_token' in r['meta'].keys():
                parameters['next_token'] = r['meta']['next_token']
                return r['data'] + self.request(request_type, query, parameters)
            return r['data']
        elif request_type == 'search':
            print(r)
            for data in r['data']:
                data['user'] = next((x for x in r['includes']['users'] if x['id'] == data['author_id']), None)
            if 'next_token' in r['meta'].keys():
                parameters['next_token'] = r['meta']['next_token']
                time.sleep(5)
                return r['data'] + self.request(request_type, query, parameters)
            return r['data']
        else:
            return r
