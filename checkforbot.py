import database
import botometer

for i in range(10000):
	
	followers = database.get_random_follower(10)

	for follower in followers:
		print(str(i) + ": " + follower.screen_name)

		rapidapi_key = ""
		twitter_app_auth = {
			'consumer_key': '',
			'consumer_secret': '',
			'access_token': '',
			'access_token_secret': '',
		}
		try:
			bom = botometer.Botometer(wait_on_ratelimit=True, rapidapi_key=rapidapi_key, **twitter_app_auth)
			result = bom.check_account(follower.user_id)
		except Exception as e:
			print(getattr(e, 'msg', '') or getattr(e, 'reason', ''))

		database.update_score(result, follower)

