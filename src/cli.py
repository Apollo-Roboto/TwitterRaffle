import argparse

def parse_arguments():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(dest='subparser')

	parser.add_argument('--conditions',
		help='What are the condition for the user to be included. Example: "like", "retweet", "reply & follow"',
		type=lambda s : s.lower(),
		required=True,
	)

	parser.add_argument('--id',
		help='The Id of the tweet',
		type=str,
		required=True,
	)

	list_parser = subparsers.add_parser('list', help='List users')

	list_parser.add_argument('--out',
		help='Output format',
		type=lambda s : s.lower(),
		choices=['json', 'stdout', 'csv'],
		default="stdout",
		required=False,
	)

	list_parser.add_argument('--file',
		help='Output file path',
		type=str,
		required=False,
	)

	pick_parser = subparsers.add_parser('pick', help='Pick a user at random')

	return parser.parse_args()