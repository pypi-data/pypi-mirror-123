from nltk.tokenize import TweetTokenizer
from twneo.config.config import TWNEO_CONFIG, get_graph_driver

TWNEO_CONFIG = TWNEO_CONFIG['TWNEO_CONFIG']
from twneo.neo4j.graph_operations import GraphOperations

class TweetsGraphCreator:

    def __init__(self):
        self.db_name = TWNEO_CONFIG['NEO4J']['database']
        self.tweet_tokenizer = TweetTokenizer()
        self.driver = get_graph_driver()
        self.graph_operations = GraphOperations()

    def create_graph(self, users , tweets , user_tweet_relations, tweet_tweet_relations):
        with self.driver.session(database=self.db_name) as session:
            for user in users:
                session.write_transaction(self.graph_operations.create_user, user  )
            for tweet in tweets:
                session.write_transaction(self.graph_operations.create_tweet, tweet  )
            for u_t_relation in user_tweet_relations:
                session.write_transaction(self.graph_operations.create_user_tweet_relation, u_t_relation  )
            for t_t_relation in tweet_tweet_relations:
                session.write_transaction(self.graph_operations.create_tweet_tweet_relation, t_t_relation  )


