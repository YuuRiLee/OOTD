import requests
import json
from urllib import parse

baseURL = "https://api.openweathermap.org/data/2.5"
apiKey = "93b13c5be1a5789936fd3e9ad6f50856"

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






