from twitter import Twitter, OAuth

"""
 Twitter Vars
"""
request_url = 'https://api.twitter.com/1.1/trends/place.json?id=1'
access_key = '717077395-OZhKTbYQPGdD2N5ZrKxsKcQN7spofhmschwLUbk1'
access_secret = 'j0rqs8UB9s7j5wI0Trs5aeKmUoQ80z9dxc8CdwQnVO3uK'
consumer_key = '5DXDPPphnJDplxrUNhIgyMSrZ'
consumer_secret = 'XhE0jiiU3cOZs7v44BQTCbGPvB3OpcT6VLzwn0SpIEqlBAHWfh'
twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))

def getTrends(event, context):

  results = twitter.trends.place(_id = 23424977)

  print "US Trends"

  for location in results:
    for trend in location["trends"]:
      print "  %s" % trend["name"].replace('#','')
