class GraphOperations:


    def create_user(self, tx, user):
        sql = """ MERGE (u:User {name: $user, userId:$userId})
           MERGE (l:Location {location : $location})
           MERGE (u)-[:lives_in]->(l)
            """
        tx.run(sql, user=user.name, location=user.location, userId=user.id, relation='lives_in')
        print(sql, user)

    def create_tweet(self, tx, tweet):
        sql = """ MERGE (t:Tweet {tweetId: $tweetId})
               """
        tx.run(sql, tweetId=tweet.tweet_id)
        if tweet.text is not None:
            sql = """ match (t:Tweet {tweetId: $tweetId})
               set t.text = $text
                           """
            tx.run(sql, tweetId=tweet.tweet_id, text=tweet.text)
            sql = """ match (t:Tweet {tweetId: $tweetId})
                          set t.retweetCount = $retweet_count
                                      """
            tx.run(sql, tweetId=tweet.tweet_id, text=tweet.text, retweet_count=tweet.retweet_count)

        print(sql, tweet)


    def create_user_tweet_relation(self, tx, user_tweet_relation):
        sql = "match (t:Tweet {tweetId: $tweetId}) " \
              "match (u:User {  userId:$userId}) " \
              f"MERGE (u)-[:{user_tweet_relation.relation_name}]->(t) "
        tx.run(sql,
               userId=user_tweet_relation.userId, tweetId=user_tweet_relation.tweetId,
               )
        print(sql, user_tweet_relation)

    def create_tweet_tweet_relation(self, tx, tweet_tweet_relation):
        sql = "match (t:Tweet {tweetId: $tweetIdfrom}) " \
              "match (u:Tweet {  tweetId:$tweetIdTo}) " \
              f"MERGE (u)-[:{tweet_tweet_relation.relation_name}]->(t) "
        tx.run(sql,
               tweetIdfrom=tweet_tweet_relation.tweetIdFrom, tweetIdTo=tweet_tweet_relation.tweetIdTo,
               )
        print(sql, tweet_tweet_relation)

    def create_tweet_tag_relation(self, tx, tweet_tag_relation):
        sql = "match (t:Tweet {tweetId: $tweetId}) " \
              "match (u:Hashtag {  tag:$tag}) " \
              f"MERGE (u)-[:{tweet_tag_relation.relation_name}]->(t) "
        tx.run(sql,
               tag=tweet_tag_relation.tag, tweetId=tweet_tag_relation.tweetId,
               )
        print(sql, tweet_tag_relation)
