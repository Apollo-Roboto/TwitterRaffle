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
	res = _request(f"tweets/{tweet_id}")
	
	if(res.status_code != 200):
		rprint(f"[red]Responded with {res.status_code}.")
		return None

	data = res.json()
	return Tweet(
		edit_history_tweet_ids=data['data']['edit_history_tweet_ids'],
		id=data['data']['id'],
		text=data['data']['text'],
	)

def get_retweeted_by(tweet_id: str, next_token: str = None) -> list[User]:

	url = f"tweets/{tweet_id}/retweeted_by"
	if next_token:
		url += f"?pagination_token={next_token}"

	res = _request(url)
	
	if(res.status_code != 200):
		rprint(f"[red]Responded with {res.status_code}.")
		return []

	data = res.json()

	users: list[User] = []

	if('data' in data):
		users.extend([
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
		users.extend(next_users)

	return users

def get_liked_by(tweet_id: str, next_token: str = None) -> list[User]:


	url = f"tweets/{tweet_id}/liking_users"
	if next_token:
		url += f"?pagination_token={next_token}"

	res = _request(url)
	
	if(res.status_code != 200):
		rprint(f"[red]Responded with {res.status_code}.")
		return []

	data = res.json()

	users: list[User] = []

	if('data' in data):
		users.extend([
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
		users.extend(next_users)

	return users