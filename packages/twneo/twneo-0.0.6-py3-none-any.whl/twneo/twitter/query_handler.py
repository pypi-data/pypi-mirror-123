from twneo.common.elements.user import User
from twneo.common.elements.tweet import   Tweet
from twneo.common.elements.user_tweet_relation import UserTweetRelation
from twneo.common.elements.tweet_tweet_relation import TweetTweetRelation

from twneo.twitter.tweet_collector import TweetCollector
from twneo.connector.graph_creator import TweetsGraphCreator

class TwitterQueryHandler:

    def __init__(self, collector = None ):
        self.collector = TweetCollector() if collector is None else collector
        self.graph_creator = TweetsGraphCreator()

    def parse_user_data(self, user_dict):
        uname = user_dict['username']
        userid = user_dict['id']
        location = user_dict['location'] if 'location' in user_dict else 'NA'
        self.user_ids.add(userid)
        return User(location = location, name= uname, id= userid)

    def parse_tweet(self, json_data):
        text = json_data['text']
        tweet_id = json_data['id']
        type = 'retweet' if text.startswith('RT @') else 'tweet'
        retweet_count = json_data['public_metrics']['retweet_count']
        return Tweet(retweet_count=retweet_count, text= text, tweet_id=tweet_id, type = type)

    def handle_tweet_search_response(self, json_resp):
        all_referenced_tweet_ids = []
        users = []
        tweets = []
        user_tweet_relations = []
        tweet_tweet_relations = []
        self.user_ids= set()
        self.missing_users = set()
        for user_dict in json_resp['includes']['users']:
            user = self.parse_user_data(user_dict)
            users.append(user)


        for json_data in json_resp['data']:
            tweet = self.parse_tweet(json_data)
            user_id = json_data['author_id']
            entities = json_data['entities']
            referenced_tweets = json_data['referenced_tweets']

            for ref_tweet in referenced_tweets :
                referenced_tweet_id = ref_tweet['id']
                tweet_tweet_rel = TweetTweetRelation(tweetIdFrom= referenced_tweet_id,tweetIdTo = tweet.tweet_id, relation_name= ref_tweet['type'])
                tweet_tweet_relations.append(tweet_tweet_rel)
                all_referenced_tweet_ids.append(referenced_tweet_id)

            tweets.append(tweet)
            mentions = entities['mentions'] if 'mentions'   in entities else []
            user_tweet_rel = UserTweetRelation(userId=user_id, tweetId=tweet.tweet_id,
                                               relation_name='tweeted')
            user_tweet_relations.append(user_tweet_rel)
            for mention in mentions:
                self.parse_mentions(json_data, mention, user_tweet_relations, users)

        start = 0
        end = 100

        # create a relation for all the referenced tweets

        while start < len(all_referenced_tweet_ids):
            ref_ids = all_referenced_tweet_ids[start:end]
            ref_tweet_details = self.collector.collect_tweets_details(ref_ids)
            start = start + 100
            end = end + 100
            for user_dict in ref_tweet_details['includes']['users']:
                user = self.parse_user_data(user_dict)
                users.append(user)

            for tweet_dict in ref_tweet_details['data']:
                tweet = self.parse_tweet(tweet_dict)
                user_tweet_rel = UserTweetRelation(userId= tweet_dict['author_id'], tweetId=tweet.tweet_id, relation_name="tweeted")
                tweets.append(tweet)
                user_tweet_relations.append(user_tweet_rel)

                entities = tweet_dict['entities']
                if 'mentions' not in entities:
                    continue
                mentions = entities['mentions']
                for mention in mentions:
                    self.parse_mentions(json_data, mention, user_tweet_relations, users)
        self.collect_missing_user_info(self.missing_users, users)

        return users, tweets, user_tweet_relations, tweet_tweet_relations

    def parse_mentions(self, json_data, mention, user_tweet_relations, users):
        relation_type = 'mentioned_in'
        user_id = mention['id']
        user_name = mention['username']
        tweetId = json_data['id']
        if user_id not in self.user_ids:
            self.missing_users.add(user_name)
        user_tweet_rel = UserTweetRelation(userId=user_id, tweetId=tweetId, relation_name=relation_type)
        user_tweet_relations.append(user_tweet_rel)

    def collect_missing_user_info(self, missing_users, users):
        result = self.collector.collect_user_details(missing_users)
        for user_data in result['data']:
            location = user_data['location'] if 'location' in user_data else 'NA'
            user = User(id=user_data['id'], name=user_data['username'], location=location)
            users.append(user)

    def handle_query(self, query = '(#byjus)'):
        self.collector.max_result_per_query = 10
        results = self.collector.collect_tweets_for_query(query, max_count=10)
        count = 0
        for json_resp in results:
            meta_data = json_resp['meta']
            count = count + meta_data['result_count']
            res = self.handle_tweet_search_response(json_resp)
            self.graph_creator.create_graph(*res)
            print(f"created for {count} records ")


if __name__ == '__main__':
    handler = TwitterQueryHandler ()
    handler.handle_query()
