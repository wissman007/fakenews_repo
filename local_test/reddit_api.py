import requests
import pandas as pd
from pprint import pprint

#'username': 'UselessJohnDoe',
#'password': 'UselessUse'
CLIENT_ID = "mV7cQmIvF_HI_f4rdB7qUQ"
SECRET_KEY = "mc8t6uX8xsdp_F67vzUdV1mzb8ElCA"

class Reddit:
    def __init__(self, CLIENT_ID, SECRET_KEY, reddit_passsword, reddit_username):
        self.client_id = CLIENT_ID
        self.secret_key = SECRET_KEY
        self.reddit_passsword = reddit_passsword
        self.reddit_username = reddit_username
        self.headers = { 'User-Agent': 'MyApp/0.0.1'}

    def get_token(self):
        data = {
            'grant_type': 'password',
            'username': self.reddit_username,
            'password': self.reddit_passsword
            }
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.secret_key)
        self.make_api_call(self.url_listing('token'),"post", token=True ,data=data, auth=auth)
        print("WE HAVE THE TOKEN")

    def make_api_call(self, url, method, token=False, **kwargs):
        response = requests.request(method= method, url= url, headers=self.headers, **kwargs)
        if token:
            if response.status_code == 200:
                print("Access token:", response.json())
            else:
                print("Error:", response.status_code, response.text)
            TOKEN = response.json().get('access_token')
            self.headers['Authorization'] = f'bearer {TOKEN}'
        return response.json()
        
    def url_listing(self, needeed_url):
        url = {
            "token": 'https://www.reddit.com/api/v1/access_token',
            "news": 'https://oauth.reddit.com/r/worldnews/new'
        }
        return url[needeed_url]

    def create_news_df(self):
        news = self.make_api_call(self.url_listing('news'), 'get')
        all_news = []
        for new in news['data']['children']:
            all_news.append({'id_news': new['data']['id'], 'title': new['data']['title'], 'url': new['data']['url'], 'author': new['data']['author']})
        df_news = pd.DataFrame(all_news)
        df_news['source'] = 'Reddit'
        return df_news

    def build_reddit(self):
        self.get_token()
        df_created = self.create_news_df()
        return df_created
    #df = pd.DataFrame(columns=['Source', 'Title', 'URL Content', 'Author', 'ID_news'])