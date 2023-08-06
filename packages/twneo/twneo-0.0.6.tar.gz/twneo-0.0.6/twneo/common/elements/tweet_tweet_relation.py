class TweetTweetRelation:

    def __init__(self, tweetIdFrom, tweetIdTo, relation_name='retweeted'):
        self.tweetIdFrom= tweetIdFrom
        self.tweetIdTo = tweetIdTo
        self.relation_name = relation_name

    def __str__(self) -> str:
        return __name__+",".join(self.__dict__.values())