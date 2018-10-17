import time
from logbook import Logger, StreamHandler, log
import sys
import pytest
import json
import requests
import configparser
import vcr


#loading the config file
config = configparser.ConfigParser()
config.read('conf.cnf')

# loading the values from the config file
apikey = config.get('API', 'MYAPIKEY')
validStatusCode = config.get('STATUSCODES', 'VALID')
baseurl = config.get('API', 'BASEURL')
api = config.get('API', 'API')
param = config.get('API', 'PARAM')

# setting up the logger
StreamHandler(sys.stdout).push_application()
log = Logger('Logbook')

# setting up the proxies
port = config.get('PORT', 'PORT')
httpproxy = config.get('PROXIES', 'HTTP')
httpsproxy = config.get('PROXIES', 'HTTPS')
proxies = {'http': httpproxy + ":" + port, 'https': httpsproxy + ":" + port}


@vcr.use_cassette()
def test_simpleGetAPIcall():

    URL_ToTest = 'https://api.ipify.org?format=json'
    # log.info('Calling the API!')
    resp = requests.get(URL_ToTest)
    # comment in the line below if you always expect a valid response
    # r.raise_for_status()

    # asserts pre-defined statusCodes
    assert int(validStatusCode) == resp.status_code

    # following two line prints the API statusCode & response in text format
    log.info(f'StatusCode from the response: {str(resp.status_code)}')
    log.info(f'API response: {resp.text}')

# following line can be used if a test needs to be skipped for some reason
# @pytest.mark.skip(reason='not used for now!')
def test_SimplePostAPIcall():
    expectedValue = 'httpbin.org'
    URL_toTest = 'https://httpbin.org/post'
    payload = {'key': 'value'}

    t0 = time.time()

    log.info(f'Calling the API!')

    resp = requests.post(URL_toTest, data=payload)
    assert validStatusCode, resp.status_code
    t1 = time.time()
    log.info(f'Found the results in {round((t1-t0), 3)} Seconds!')
    APIResponse = json.loads(resp.text)
    items = APIResponse['headers']
    # go through the elements in the JSON payload and find the expected value
    assert expectedValue, items['Host']

