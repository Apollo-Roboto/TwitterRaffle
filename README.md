# Twitter Raffle

Create a `.env` file containing the twitter developer token and credentials.

```env
APP_ID=
API_KEY=
API_KEY_SECRET=
BEARER_TOKEN=
```

## How to use

Examples:
```bash
python ./src/main.py --id="<tweet_id>" --conditions="like" list
python ./src/main.py --id="<tweet_id>" --conditions="like retweet" pick
python ./src/main.py --id="<tweet_id>" --conditions="retweet like" list --out="csv"
```

### Modes

`list`: Lists all the user matching the conditions of the raffle.

`pick`: Pick one random user from the list of users matching the conditions of the raffle.

### Parameters

`id`: required, The tweet id, you can find it at the end of the tweet url.

`conditions`: required, Conditions of the raffle, current options are `like` and `retweet`.

`out`: Chosses the output format for the list , options: `json`, `csv`, `stdout`.

`file`: File path for the user list (when `out` is not `stdout`).