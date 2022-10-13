from rich import print as rprint
import dotenv
import twitterService
import json
from models import CustomEncoder, User
import random
import cli
import csv

args = cli.parse_arguments()

def save_json(users: User, path: str):
	with open(path, 'w', encoding='UTF-8') as f:
		json.dump(users, f, cls=CustomEncoder, ensure_ascii=False)

def save_csv(users: User, path: str):
	file = open(path, 'w', encoding='UTF-8', newline='') # newline is to avoid writing whitespace
	writer = csv.writer(file)

	# Write headers
	writer.writerow(['id', 'name', 'username'])

	# Write rows
	for user in users:
		writer.writerow([user.id, user.username, user.name])

	file.close()

def print_users(users: User):
	rprint('\n[yellow bold]Id                        Username                  Name ')
	rprint('')

	for user in users:
		rprint(f'{user.id:<25} {user.username:<25} {user.name}')

def main():
	dotenv.load_dotenv()

	users = []

	# space seperated list of conditions to a set
	conditions = set(args.conditions.split(' '))

	if conditions == {'retweet'}:
		users = twitterService.get_retweeted_by(args.id)

	elif conditions == {'like'}:
		users = twitterService.get_liked_by(args.id)

	elif conditions == {'like', 'retweet'}:
		retweet_users = twitterService.get_retweeted_by(args.id)
		like_users = twitterService.get_liked_by(args.id)

		for user in retweet_users:
			if user in like_users:
				users.append(user)
	else:
		rprint(f'[red]Unknown conditions \'{args.conditions}\'')
		exit(1)

	rprint(f'[green]Collected {len(users)} users')

	if args.subparser == 'list':
	
		if args.out == 'json':
			file = args.file if args.file else './users.json'
			print('Saving users to ' + file)
			save_json(users, file)
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
		choice = random.choice(users)
		rprint(f"[yellow bold]\n✨{choice}\n")

if(__name__ == '__main__'):
	main()