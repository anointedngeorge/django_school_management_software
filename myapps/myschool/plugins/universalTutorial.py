import requests


def getAccessToken(apiToken=None, email=None):
    try:
        url = "https://www.universal-tutorial.com/api/getaccesstoken"
        headers = {
            "Accept": "application/json",
            "api-token": f"{apiToken}",
            "user-email": f"{email}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200: 
            return {"data":response.json(), "status":True}
        else:
            return {"data":None, "status":False}
        
    except Exception as e:
        return {"data":str(e), "status":False}



def getCountries(accessToken):
    try:
        url = "https://www.universal-tutorial.com/api/countries/"
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {"data":response.json(), "status":True}
        else:
            return {"data":None, "status":False}
        
    except Exception as e:
        return {"data":str(e)}

# print(getCountries())


def getStates(accessToken, country_name):
    try:
        url = f"https://www.universal-tutorial.com/api/states/{country_name}"
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {"data":response.json(), "status":True}
        else:
            return {"data":None, "status":False}
        
    except Exception as e:
        return {"data":str(e)}
# print(getStates())


def getCities(accessToken='', state_name=''):
    try:
        url = f"https://www.universal-tutorial.com/api/cities/{state_name}"
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {"data":response.json(), "status":True}
        else:
            return {"data":None, "status":False}
        
    except Exception as e:
        return {"data":str(e)}


