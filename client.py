import requests
import json

class Settings(object):
    netid = 'sdadi2'
    API_key = 'b80807d400c5'

    # netid = 'jaj5'
    # API_key = '7e5bcace6b50'
    base_url = 'https://jweible.web.illinois.edu/pz-server/games/'

class SuccessResponse(object):
    def __init__(self, obj):
        self.status_code = obj.status_code
        self.content = json.loads(obj.content).get('result')

class FailureResponse(object):
    def __init__(self, obj):
        self.status_code = obj.status_code
        self.content = obj.content

    def __str__(self):
        return 'Failed with error code: {} and message as {}'.format(self.status_code, self.content)

class Client(object):
    def __init__(self, netid=None, API_key=None):
        self.netid = netid or Settings.netid
        self.API_key = API_key or Settings.API_key
        self.base_url = Settings.base_url
        self.json_data = {'netid': self.netid, 'player_key': self.API_key}
        self.session = self.fetch_session()

    def raise_error(self, err):
        raise Exception(str(FailureResponse(err)))

    def fetch_session(self):
        s = requests.Session()
        s.headers = {"Connection": "close"}
        return s

    def fetch_game_types(self):
        endpoint = self.base_url + 'game-types'
        r = self.session.get(endpoint, json=self.json_data)
        return SuccessResponse(r) if r.status_code == 200 else self.raise_error(r)

    def move(self, move, match_id):
        endpoint = self.base_url + 'match/{}/move'.format(match_id)
        s = requests.Session()
        json_data = self.json_data
        json_data['move'] = move
        r = s.post(url=endpoint, json=json_data)
        return SuccessResponse(r) if r.status_code == 200 else self.raise_error(r)

    def fetch_match_id(self, game_id):
        endpoint = self.base_url + '/game-type/{}/request-match'.format(game_id)
        r = self.session.post(endpoint, json=self.json_data)
        return SuccessResponse(r) if r.status_code == 200 else self.raise_error(r)

    def fetch_game_details(self, game_id):
        endpoint = self.base_url + 'game-type/{}/details'.format(game_id)
        r = self.session.get(endpoint, json=self.json_data)
        return SuccessResponse(r) if r.status_code == 200 else self.raise_error(r)

    def resign_match(self, match_id):
        endpoint = self.base_url + 'match/{}/resign'.format(match_id)
        s = requests.Session()
        json_data = self.json_data
        json_data['match_id'] = match_id
        r = s.post(endpoint, json=json_data)
        return SuccessResponse(r) if r.status_code == 200 else self.raise_error(r)

    def fetch_turn(self, match_id):
        endpoint = self.base_url + 'match/{}/await-turn'.format(match_id)
        r = self.session.get(url=endpoint)
        return SuccessResponse(r) if r.status_code == 200 else self.raise_error(r)


    def fetch_match_history(self, match_id):
        endpoint = self.base_url + '/match/{}/history'.format(match_id)
        r = self.session.get(url=endpoint)
        return SuccessResponse(r) if r.status_code == 200 else self.raise_error(r)
