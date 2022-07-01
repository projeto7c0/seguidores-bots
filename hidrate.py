import twitter
import database
import sys

followers = database.get_followers()

while (len(followers) > 0):
	twitter.hidrate_ids(followers)
	followers = database.get_followers()