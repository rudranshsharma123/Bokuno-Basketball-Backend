from os import defpath
from numpy import diff
import requests
from urllib.request import Request, urlopen


# url = "https://api.pexels.com/v1/search?query=basketball&per_page=100"
# api_token = "563492ad6f917000010000019b0c05ab5204447bbfe5189198fa2166"
# headers = {
#     "Authorization":api_token,
    
# }
# v = 10
# req = requests.get(url= url, headers=headers)
# res = req.json()
# imagesList = res['photos']
# images = []
def fetchImages():
    for v, i in enumerate(imagesList):
        re = requests.get(i["src"]['tiny'],headers= {'User-Agent': 'Mozilla/5.0'} )
        with open('{k}.jpg'.format(k = v), "wb") as f:
            f.write(re.content)
def fetchCaptions():
    data = {"name":[], "captions":[]}
    for v, i in enumerate(imagesList):
        x = str(i["url"])
        y = " ".join(x.replace("https://www.pexels.com/photo/", "").split('-')[:-1])
        data['name'].append('{k}.jpg'.format(k = v))
        data["captions"].append(y)
    import pandas as pd
    df = pd.DataFrame(data= data)
    df.to_csv('caption1s.csv')

def win():
    sel = '#loadmore'
    url = "https://www.wisdomjobs.com/e-university/basketball-interview-questions.html"
    from requests_html import HTMLSession
    print(url)
    session = HTMLSession()
    response = session.get(url)
    raw_reponse = response.html.find('.interview_questions', first = True).text
    data = {}
    x = [x for x in raw_reponse.split('\n') if "else" not in x]
    print(x)
    for i, v in enumerate(x):
        if v.startswith("Question"):
            data[v] = []
            while i+1 < len(x) and not x[i+1].startswith("Question"):
                data[v].append(x[i+1])
                i+=1
            data[v] = "\n".join(data[v])
    import pandas as pd
    col = list(data.keys())
    ind = list(data.values())
    d = {'question' :[], 'ans' : [], 'website':url}
    for i, v in enumerate(col):
        d['question'].append(v)
        d['ans'].append(ind[i])
    df = pd.DataFrame(data= d)
    df.to_csv("t2est.csv")

win()