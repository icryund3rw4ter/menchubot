# Introduction

This is a basic Python3 port of tommeagher's ebook's bot (https://github.com/tommeagher/heroku_ebooks) and gabubonico's (https://github.com/gabubonico/gabubot_ebooks) self-hosting solution. 

I've made this project to be ran on Python 3. Didn't work for me with previous versions.

## Setup
0. Be sure to have Python 3 installed.

1. Clone this repo.

2. If posting to Twitter, create a Twitter account that you will post to.

3. Install the libraries python-twitter, Mastodon.py and beautifulsoup4. You can do this by doing:
```
pip3 install python-twitter
pip3 install Mastodon.py
pip3 install beautifulsoup4
```
5. Sign into https://dev.twitter.com/apps with the same login and create an application. Make sure that your application has read and write permissions to make POST requests. This is done by Going to 'User authentication settings' and choosing OAuth 1.0.

6. Once you're finished setting up the Twitter App, go to 'Keys and tokens' and reveal the API, the API secret key, the Twitter access token, and the secret access token. Copy these keys.

7. Edit `local_settings.py` and paste the keys following the instructions below:
```
MY_CONSUMER_KEY = ' '   #Introduce the API key between the single quotes.
MY_CONSUMER_SECRET = ' '  #Introduce the API secret key between the single quotes.
MY_ACCESS_TOKEN_KEY = ' '   #Introduce the access token key between the single quotes.
MY_ACCESS_TOKEN_SECRET = ' '  #Introduce the access token secret key between the single quotes.
```

8. In `local_settings.py`, set `ENABLE_TWITTER_SOURCES` and `ENABLE_TWITTER_POSTING` to `True`. Also be sure to add the handle of the Twitter user you want your _ebooks_ account to be based on in `TWITTER_SOURCE_ACCOUNTS`. It should be a list of comma-separated, quote-enclosed usernames (if you only want it to be based on one user, then there is no need to use the commas). For example:
```
TWITTER_SOURCE_ACCOUNTS = ["jack","nytimes"]      
```

10. Additionally, set the twitter account that you created in order for the bot to post the tweets in `TWEET_ACCOUNT` (write the the username without the @). Example:
```
TWEET_ACCOUNT = "my_bot_account"
```

11. If you want to modify the behaviour of the bot, you can change the `ODDS` and `ORDER` parametres, although I would leave it as it is.

12. To make your tweets go live, change the `DEBUG` variable to `False`.

## Running the bot
If you're on Linux, I recommend going into the folder of the repo, open a terminal, and do:
```
chmod +x *
```
This is done in order to give execution permissions to all the files inside the folder.

Time to run the bot. You can do it by running (if you're on Linux):
```
python3 ebooks.py
```
This will post only a tweet. 

How can you make it so it tweets every 30 minutes? (for example).

You can run the `timer.sh` script by doing `./timer.sh`. However, it wasn't working for me so another way to do it is by using `crontab` (this is for Linux, don't know if there's any similar program for Windows), which is a daemon. Cron will check if there is any task (job) to be executed, according to the time configured in the operating system itself. To create this task, we first have to start the cron service by running
```
systemctl start cron
```
and then we create the task with
```
crontab -e
```
Then, we go to the last line of the file and paste the code below. You should replace '/home/pi/Documents/menchubot' with the route of the cloned repo.
```
*/30 * * * * cd /home/pi/Documents/menchubot && python3 ebooks.py  >/dev/null 2>&1
```

If you want it to run every 45 minutes, you can change the 30 for 45. You can also check other options (like make it run the first hour of the day, which days, etc.) by looking at the manual in https://linux.die.net/man/5/crontab.

## Credit
This is based almost entirely on tommeagher's ebook's bot (https://github.com/tommeagher/heroku_ebooks). All the credit goes to him and gabubonico's (https://github.com/gabubonico/gabubot_ebooks) for the tweaks and the self-hosting solution he's given. As a result, all of the blame for clunky implementation in Python3 fall on me.
