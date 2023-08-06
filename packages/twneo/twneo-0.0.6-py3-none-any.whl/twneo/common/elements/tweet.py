class Tweet :


    def __init__(self,retweet_count  , text   , tweet_id  , type    ):
        self.text= text
        self.tweet_id=tweet_id
        self.type = type
        self.retweet_count=str(retweet_count)


    def __str__(self) -> str:
        return __name__+",".join(self.__dict__.values())