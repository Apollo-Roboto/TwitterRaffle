from dataclasses import dataclass

@dataclass
class User:
	id: str
	name: str
	username: str

	def __hash__(self):
		return hash(repr(self))