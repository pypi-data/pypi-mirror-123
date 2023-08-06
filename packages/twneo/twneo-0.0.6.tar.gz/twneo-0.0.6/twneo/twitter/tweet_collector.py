import requests
import os
import json
from twneo.config.config import TWNEO_CONFIG

TWNEO_CONFIG = TWNEO_CONFIG['TWNEO_CONFIG']
bearer_token = TWNEO_CONFIG['twitter_bearer_tocken']

class TweetCollector:

    def __init__(self):
        self.search_url = "https://api.twitter.com/2/tweets/search/recent"
        self.max_result_per_query = '10'

    def get_params(self, query):
        return {'query': query,
                "tweet.fields": ["public_metrics,entities,referenced_tweets"],
                "user.fields": ["location"], "expansions": "author_id",
                'max_results': self.max_result_per_query, }

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2FullArchiveSearchPython"
        return r

    def connect_to_endpoint(self, url, params):

        response = requests.request("GET", url, auth=self.bearer_oauth, params=params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def collect_tweets_for_query(self, query, max_count=100):
        result = []

        params = self.get_params(query)
        # self.search_url = self.search_url + "?tweet.fields=public_metrics,entities"
        json_resp = self.connect_to_endpoint(self.search_url, params=params)
        result.append(json_resp)
        meta_data = json_resp['meta']
        count = meta_data['result_count']

        while 'next_token' in meta_data:
            if count >= max_count:
                break
            params['next_token'] = meta_data['next_token']
            json_resp = self.connect_to_endpoint(self.search_url, params=params)
            result.append(json_resp)
            count = count + meta_data['result_count']

        return result

    def collect_tweets_details(self, tweet_ids):
        params = {'ids': ','.join(tweet_ids),
                  "tweet.fields": ["public_metrics,entities,referenced_tweets"],
                  "user.fields": ["location,username"], "expansions": "author_id",
                  }
        search_url = 'https://api.twitter.com/2/tweets'
        result = self.connect_to_endpoint(search_url, params)
        return result

    def create_url(user_names_list, user_fields):
        # Specify the usernames that you want to lookup below
        # You can enter up to 100 comma-separated values.
        user_names = ','.join(user_names_list) if len(user_names_list) > 1 else user_names_list[0]

        usernames = f"usernames={user_names}"
        url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
        print(url)
        return url


    def collect_user_details(self, user_names_list):
        user_names = ','.join(user_names_list) if len(user_names_list) > 1 else user_names_list[0]
        params = {'usernames': user_names, "user.fields": ["location,username"]}
        url = "https://api.twitter.com/2/users/by"
        result = self.connect_to_endpoint(url, params)
        return result