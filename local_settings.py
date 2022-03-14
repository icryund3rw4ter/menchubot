from os import environ

# Configuration for Twitter API
ENABLE_TWITTER_SOURCES = True   # Fetch twitter statuses as source
ENABLE_TWITTER_POSTING = True   # Tweet resulting status?
MY_CONSUMER_KEY = 'Introduce consumer key'                         # Your Twitter API Consumer Key
MY_CONSUMER_SECRET = 'Introduce consumer secret key'               # Your Consumer Secret Key
MY_ACCESS_TOKEN_KEY = 'Introduce API access token key'             # Your Twitter API Access Token Key
MY_ACCESS_TOKEN_SECRET = 'Introduce API access token secret key'   # Your Access Token Secret

# Sources (Twitter or a local text file)
TWITTER_SOURCE_ACCOUNTS = [" "]  # A list of comma-separated, quote-enclosed Twitter handles of account that you'll generate tweets based on. It should look like ["account1", "account2"]. If you want just one account, no comma needed.
SOURCE_EXCLUDE = r'^$'  # Source tweets that match this regexp will not be added to the Markov chain. You might want to filter out inappropriate words for example.
STATIC_TEST = False  # Set this to True if you want to test Markov generation from a static file instead of the API.
TEST_SOURCE = ".txt"  # The name of a text file of a string-ified list for testing. To avoid unnecessarily hitting Twitter API. You can use the included testcorpus.txt, if needed.

ODDS = 2  # How often do you want this to run? 1/8 times?
ORDER = 2  # How closely do you want this to hew to sensical? 2 is low and 4 is high.

DEBUG = True  # Set this to False to start Tweeting live
TWEET_ACCOUNT = " "  # The name of the account you're tweeting to (without @)

#Configuration for Twitter parser
TWITTER_ARCHIVE_NAME = "tweets.csv" #Name of your twitter archive
IGNORE_RETWEETS = True #If you want to remove retweets
