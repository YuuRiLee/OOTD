import requests
import json
from urllib import parse

baseURL = "https://api.openweathermap.org/data/3.0"
apiKey = "8df2382f012dcc669d0c188c128e2a49"


# baseURL + query parameter 조합
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






