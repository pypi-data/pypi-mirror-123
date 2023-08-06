import os
from twneo.twitter.query_handler import TwitterQueryHandler
os.environ['twneo_config_path'] = r'/Users/pankaj/dev/git/twneo/twneo/config/config_dev.yaml'


from twneo.twitter.tweet_collector import TweetCollector
from twneo.connector.graph_creator import TweetsGraphCreator


def main():
    query = '(#byjus)'
    if __name__ == '__main__':
        handler = TwitterQueryHandler()
        handler.handle_query(query= query)

if __name__ == '__main__':
    main()