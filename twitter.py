import twitter_auth
import json
import tweepy
import database


def get_accounts_from_list():
    client = twitter_auth.authenticate_v2()
    with open("seguidores_politicos/config.json") as jsonfile:
        list = json.load(jsonfile)['list']

    response = client.get_list_members(id = int(list['id']),  user_fields = 'public_metrics')

    for account in response.data: 
        database.upsert_account(account)

    return 


def get_all_followers(account):
    api = twitter_auth.authenticate_v1(account.bearer_token)

    for response in tweepy.Cursor(api.get_follower_ids, user_id=account.account_id, count=5000).pages():
        database.insert_follower_list_id(response, account)

    return


def hidrate_ids(followers):
    client = twitter_auth.authenticate_v2()

    ids_f = []
    for follower in followers:
        ids_f.append(follower.user_id) 

    users = client.get_users(ids=ids_f, user_fields='created_at')
    database.update_users(users)

    return