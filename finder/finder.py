from pyhunter import PyHunter
import requests,urllib.parse,collections

def hunter(first_name, last_name, company_name, url, API):
    hunter = PyHunter(API)
    email,score = hunter.email_finder(first_name=first_name,last_name=last_name,company=company_name)
#     if confidence_score < 75:
#         return ""
    return email

def anymail(first_name, last_name, company_name, domain, API):
    url = "https://api.anymailfinder.com/v3.1/search/person.json"
    data = {
        "name":first_name + " " + last_name,
        "domain":domain, }
    headers = { 'X-Api-Key': API, }
    email = ""
    r = requests.post(url,json=data,headers=headers)
    if r:
        print(r.status_code)
        if r.status_code == 200:
            email = r.json()['best_guess']
    print("email: " + email)
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
    print("email: " + email)
    return email
