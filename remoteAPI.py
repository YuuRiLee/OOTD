import requests
import json
from urllib import parse

baseURL = "https://api.openweathermap.org/data/3.0"
apiKey = "7ad356131f12d62cacbb82e63b5871f3"

def buildAPIURL(path, parameters):
    url = baseURL + path + "?"
    query = {
        "appid": apiKey
    }
    query.update(parameters)
    queryString = parse.urlencode(query)
    # for debug
    print(url + queryString)
    return url + queryString

def getRequest(path, parameters):
    response = requests.get(buildAPIURL(path, parameters))
    return response






