from rich import print as rprint
import dotenv
import twitterService
import json
from models import CustomEncoder, User
import random
import cli
import csv

args = None

def save_json(users: list[User], path: str):
	with open(path, 'w', encoding='UTF-8') as f:
		json.dump(users, f, cls=CustomEncoder, ensure_ascii=False)

def save_csv(users: list[User], path: str):
	file = open(path, 'w', encoding='UTF-8', newline='') # newline is to avoid writing whitespace
	writer = csv.writer(file)

	# Write headers
	writer.writerow(['id', 'name', 'username'])

	# Write rows
	for user in users:
		writer.writerow([user.id, user.username, user.name])

	file.close()

def print_users(users: list[User]):
	rprint('\n[yellow bold]Id                        Username                  Name ')
	rprint('')

	for user in users:
		rprint(f'{user.id:<25} {user.username:<25} {user.name}')
	
	rprint('')

def fill_or_intersect(set1: set, set2: set):
	if len(set1) == 0:
		return set2
	else:
		return set1.intersection(set2)

def main():

	users = set()

	# space seperated list of conditions to a set
	conditions = set(args.conditions.split(' '))

	if 'retweet' in conditions:
		users = fill_or_intersect(users, twitterService.get_retweeted_by(args.id))

	if 'like' in conditions:
		users = fill_or_intersect(users, twitterService.get_liked_by(args.id))

	if 'reply' in conditions:
		rprint('[yellow bold]The condition \'reply\' is limited to the last 7 days, this might ignore some users.')
		tweet = twitterService.get_tweet(args.id)
		users = fill_or_intersect(users, twitterService.get_replied_by(tweet.conversation_id))

	rprint(f'[green]Collected {len(users)} users')

	if args.subparser == 'list':
	
		if args.out == 'json':
			file = args.file if args.file else './users.json'
			print('Saving users to ' + file)
			save_json(tuple(users), file)
			rprint('[green]Saved!')
			
		elif args.out == 'csv':
			file = args.file if args.file else './users.csv'
			print('Saving users to ' + file)
			save_csv(users, file)
			rprint('[green]Saved!')

		elif args.out == 'stdout':
			print_users(users)

		else:
			rprint(f'[red]Unknown format \'{args.out}\'')
			exit(1)
	
	elif args.subparser == 'pick':
		choice = random.choice(tuple(users))
		rprint(f"[yellow bold]\n✨ {choice}\n")

if(__name__ == '__main__'):
	args = cli.parse_arguments()
	dotenv.load_dotenv()
	main()