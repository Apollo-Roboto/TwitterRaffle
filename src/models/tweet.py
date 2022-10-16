from dataclasses import dataclass

@dataclass
class Tweet:
	edit_history_tweet_ids: list[str]
	id: str
	text: str
	conversation_id: str
	author_id: str
	has_attachments: bool