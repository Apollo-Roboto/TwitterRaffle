import requests
import os
from models import Tweet, User
from rich import print as rprint

base_url = "https://api.twitter.com/2/"

def _request(url: str):
	full_url = base_url + url

	rprint(f'[grey27]GET {full_url}')

	return requests.get(full_url,
		headers={
			"Authorization": "Bearer " + os.environ["BEARER_TOKEN"]
		}
	)

def get_tweet(tweet_id: str) -> Tweet:
	res = _request(f'tweets?ids={tweet_id}&tweet.fields=conversation_id,author_id,attachments')
	
	if(res.status_code != 200):
		rprint(f"[red]Responded with {res.status_code}.")
		return None

	data = res.json()

	if(len(data['data']) < 1):
		raise Exception(f'No data for tweet id \'{tweet_id}\'')

	return Tweet(
		edit_history_tweet_ids=data['data'][0]['edit_history_tweet_ids'],
		id=data['data'][0]['id'],
		text=data['data'][0]['text'],
		conversation_id=data['data'][0]['conversation_id'],
		author_id=data['data'][0]['author_id'],
		has_attachments=('attachments' in data['data'][0]),
	)

def get_tweet_replies(conversation_id: str, next_token: str = None) -> list[Tweet]:

	url = f'tweets/search/recent?query=conversation_id:{conversation_id}&tweet.fields=conversation_id,author_id,attachments'
	# the 'all' endpoint is limited to the Academic Research access. 'recent' only includes the last 7 days.
	if next_token:
		url += f'&pagination_token={next_token}'

	res = _request(url)
	
	if(res.status_code != 200):
		rprint(f'[red]Responded with {res.status_code}.')
		return None

	data = res.json()

	tweets: list[Tweet] = []

	if('data' in data):
		tweets.extend([
			Tweet(
				edit_history_tweet_ids=tweet['edit_history_tweet_ids'],
				id=tweet['id'],
				text=tweet['text'],
				conversation_id=tweet['conversation_id'],
				author_id=tweet['author_id'],
				has_attachments=('attachments' in tweet),
			)
			for tweet in data['data']
		])

	has_next = 'meta' in data and 'next_token' in data['meta']

	if has_next:
		next_token = data['meta']['next_token']
		next_tweets = get_tweet_replies(conversation_id, next_token)
		tweets.extend(next_tweets)

	return tweets
	
def get_replied_by(conversation_id: str, next_token: str = None) -> set[User]:

	url = f'tweets/search/recent?query=conversation_id:{conversation_id}&user.fields=id,name,username&expansions=author_id'
	# the 'all' endpoint is limited to the Academic Research access. 'recent' only includes the last 7 days.
	if next_token:
		url += f'&pagination_token={next_token}'

	res = _request(url)
	
	if(res.status_code != 200):
		rprint(f'[red]Responded with {res.status_code}.')
		return None

	data = res.json()

	users: set[User] = set()

	if('includes' in data):
		users.update([
			User(
				id=user['id'],
				name=user['name'],
				username=user['username'],
			)
			for user in data['includes']['users']
		])

	has_next = 'meta' in data and 'next_token' in data['meta']

	if has_next:
		next_token = data['meta']['next_token']
		next_users = get_replied_by(conversation_id, next_token)
		users.update(next_users)

	return users

def get_retweeted_by(tweet_id: str, next_token: str = None) -> set[User]:

	url = f"tweets/{tweet_id}/retweeted_by"
	if next_token:
		url += f"?pagination_token={next_token}"

	res = _request(url)
	
	if(res.status_code != 200):
		rprint(f"[red]Responded with {res.status_code}.")
		return None

	data = res.json()

	users: set[User] = set()

	if('data' in data):
		users.update([
			User(
				id=user['id'],
				name=user['name'],
				username=user['username'],
			)
			for user in data['data']
		])

	# For pagination, get the next page's users
	has_next = 'meta' in data and 'next_token' in data['meta']

	if has_next:
		next_token = data['meta']['next_token']
		next_users = get_retweeted_by(tweet_id, next_token)
		users.update(next_users)

	return users

def get_liked_by(tweet_id: str, next_token: str = None) -> set[User]:

	url = f"tweets/{tweet_id}/liking_users"
	if next_token:
		url += f"?pagination_token={next_token}"

	res = _request(url)
	
	if(res.status_code != 200):
		rprint(f"[red]Responded with {res.status_code}.")
		return None

	data = res.json()

	users: set[User] = set()

	if('data' in data):
		users.update([
			User(
				id=user['id'],
				name=user['name'],
				username=user['username'],
			)
			for user in data['data']
		])

	# For pagination, get the next page's users
	has_next = 'meta' in data and 'next_token' in data['meta']

	if has_next:
		next_token = data['meta']['next_token']
		next_users = get_liked_by(tweet_id, next_token)
		users.update(next_users)

	return users