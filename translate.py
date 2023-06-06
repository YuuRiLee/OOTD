import json
import urllib.request
import ssl

clientId = "1DsokuxBgDVkvRTwJ3bf" # 개발자센터에서 발급받은 Client ID 값
clientSecret = "qj0jWU5DYc" # 개발자센터에서 발급받은 Client Secret 값

# SSL 인증서 검증 무시
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

url = "https://openapi.naver.com/v1/papago/n2mt"
request = urllib.request.Request(url)

request.add_header("X-Naver-Client-Id", clientId)
request.add_header("X-Naver-Client-Secret", clientSecret)

def translateText(text):
  encText = urllib.parse.quote(text)
  data = "source=en&target=ko&text=" + encText
  response = urllib.request.urlopen(request, data=data.encode("utf-8"), context=context)
  rescode = response.getcode()
  if(rescode==200):
    responseBody = response.read().decode('utf-8')
    decode = json.loads(responseBody)
    result = decode['message']['result']['translatedText']
    return result
  else:
    print("Error Code:" + rescode)
    return text
