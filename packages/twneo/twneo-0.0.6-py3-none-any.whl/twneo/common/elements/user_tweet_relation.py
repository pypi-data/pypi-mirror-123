class UserTweetRelation:

    def __init__(self, userId, tweetId, relation_name='retweets'):
        self.userId= userId
        self.tweetId = tweetId
        self.relation_name = relation_name

    def __str__(self) -> str:
        return __name__+",".join(self.__dict__.values())