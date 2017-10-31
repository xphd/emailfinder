from pyhunter import PyHunter
import requests,urllib.parse,collections

def hunter(first_name, last_name, company_name, API):
    hunter = PyHunter(API)
    email = ""
    score = 0
    email,score = hunter.email_finder(first_name=first_name,last_name=last_name,company=company_name)
    if type(email) != type(""):
        email = 'Person Not Found'
    if type(score) != type(0):
        score = -1
    return email,score

def anymail(first_name, last_name, company_name, domain, API):
    url = "https://api.anymailfinder.com/v3.1/search/person.json"
    data = {
        "name":first_name + " " + last_name,
        "domain":domain, }
    headers = { 'X-Api-Key': API, }
    email = ""
    r = requests.post(url,json=data,headers=headers)
    # print(r.statue_code)
    if r.status_code == 200:
        email = r.json()['best_guess']
        print(email)
    else:
        print("Person Not Found",r.status_code)
        email = 'Person Not Found'
    return email

def rocketreach(first_name, last_name, company_name, API):
    base_url = "https://api.rocketreach.co/v1/api"
    end_point = "/lookupProfile?"
    params = [
        ('api_key',API),
        ('name', first_name + " " + last_name),
        ('current_employer',company_name), ]
    params = collections.OrderedDict(params)
    url = base_url + end_point + urllib.parse.urlencode(params)
    r = requests.get(url)
    email = ""
    if r.status_code == 200:
         email = r.json()[0]['current_work_email']
         if type(email) != type(''):
             email = 'None'
    else:
        print("Person Not Found",r.status_code)
        email = "Person Not Found"
    return email
