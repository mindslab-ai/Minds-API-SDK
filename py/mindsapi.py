# -*- coding: utf-8 -*-
import requests
import json
import os

STT_VERSION = "0.1.0"
API_FRONT_URL = "http://127.0.0.1:8000/api/stt/"
# API_FRONT_URL = "http://35.162.66.180/api/stt/"
MINDS_API_ID = "minds_api_id"
MINDS_API_KEY = "minds_api_key"


class AudioFileSttClient(object):

    def __init__(self, ID=None, key=None, lang=None, level=None, sampling=None):
        self.version = STT_VERSION
        self.ID = ID
        self.key = key
        self.lang = lang
        self.level = level
        self.sampling = sampling

    def __version__(self):
        return self.version

    def putID(self, ID):
        self.ID = ID

    def getID(self):
        return self.ID

    def putKey(self, key):
        self.key = key

    def getKey(self):
        return self.key

    def putSttModel(self, lang=None, level=None, sampling=None):
        self.lang = lang
        self.level = level
        self.sampling = sampling

    def getSttModel(self):
        return self.lang, self.level, self.sampling

    def CheckAvailableSttModels(self, _print=True):
        data = {'cmd': 'getSttModels', 'ID': self.ID, 'key': self.key}
        files = {}
        r = requests.post(API_FRONT_URL, files=files, data=data)
        if r.status_code == 200:
            r_dict = json.loads(r.text)
            status = r_dict['status']
            if status == 'Success':
                data = json.loads(r_dict['data'])
            else:
                data = r_dict['data']
            if _print:
                print(json.dumps(data, indent=4, sort_keys=True))
            return status, data
        else:
            return 'Fail', 'Error code : ' + r.status_code

    def RunFileStt(self, audioFilename, _print=True):
        if not os.path.isfile(audioFilename):
            return 'Fail', 'File not found'

        data = {'cmd': 'runFileStt', 'lang': self.lang, 'sampling': self.sampling, 'level': self.level, 'ID': self.ID,
                'key': self.key}
        files = {'file': open(audioFilename, 'rb')}
        r = requests.post(API_FRONT_URL, data=data, files=files)
        if r.status_code == 200:
            r_dict = json.loads(r.text)
            if _print:
                print(r_dict['status'] + ' : ' + r_dict['data'])
            return r_dict['status'], r_dict['data']
        else:
            return 'Fail', str(r.status_code)


def test():

    stt = AudioFileSttClient()

    stt.putID(MINDS_API_ID)
    print("\n # ID  : " + stt.getID())

    stt.putKey(MINDS_API_KEY)
    print("\n # Key : " +  stt.getKey())

    status, data = stt.CheckAvailableSttModels(_print=False)
    print("\n # Response : {}".format(status))
    if status == 'Success':
        print(" > The number of available STT models : {:d}".format(len(data['sttModels'])))
        print(json.dumps(data, indent=4, sort_keys=True))
    else:
        print(" > " + data)
        return

    sttModel = data['sttModels'][0]
    stt.putSttModel(lang=sttModel['lang'], level=sttModel['level'], sampling=sttModel['sampling'])
    sttModel = stt.getSttModel()
    print("\n # STT Model: {}-{}-{}".format(sttModel[1], sttModel[0], sttModel[2]))

    status, data = stt.RunFileStt('8k.pcm', _print=False)

    print("\n # RunFileStt - " + status + " : " + data)

    pass


if __name__ == "__main__":

    test()
