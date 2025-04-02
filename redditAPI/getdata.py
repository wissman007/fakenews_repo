import requests
import pandas as pd

CLIENT_ID = "mV7cQmIvF_HI_f4rdB7qUQ"
SECRET_KEY = "mc8t6uX8xsdp_F67vzUdV1mzb8ElCA"

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
data = {
    'grant_type': 'password',
    'username': 'UselessJohnDoe',
    'password': 'UselessUse'
    }
headers = { 'User-Agent': 'MyApp/0.0.1' }
url = 'https://www.reddit.com/api/v1/access_token'
response = requests.post(url, auth=auth, data=data, headers=headers)
if response.status_code == 200:
    print("Access token:", response.json())
else:
    print("Error:", response.status_code, response.text)
TOKEN = response.json().get('access_token')
headers['Authorization'] = f'bearer {TOKEN}'

res = requests.get('https://oauth.reddit.com/r/worldnews/new', headers=headers)
df = pd.DataFrame(columns=['Source', 'Title', 'URL Content', 'Author', 'ID_news'])
for post in res.json()['data']['children']:
    new_data = pd.DataFrame([{
    'Source' : 'Reddit',
    'Title' : post['data']['title'],
    'URL Content' : post['data']['url'],
    'Author' : post['data']['author'],
    'ID_news' : post['data']['author'] + ' ' + post['data']['title'],
}])
    df = pd.concat([df, new_data], ignore_index=True)