import twitter
import database
import sys

candidate = sys.argv[1]

accounts_tw = twitter.get_accounts_from_list()
account_db = database.get_account_details(candidate)

print(account_db)

twitter.get_all_followers(account_db)