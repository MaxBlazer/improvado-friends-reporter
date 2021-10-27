import requests
import json


def get_friends(token, user_id=0) -> list:
    url = f'https://api.vk.com/method/friends.get?v=5.81&access_token={token}&fields=&user_id={user_id}'
    response = requests.get(url)
    return json.loads(response.text)['response']['items']


def get_users(token, user_ids) -> dict:
    url = f"https://api.vk.com/method/users.get?v=5.81&access_token={token}&user_ids={','.join(str(id) for id in user_ids)}"
    response = requests.get(url)
    return json.loads(response.text)


def main():
    access_token = input('Enter access token: ')
    user_id = 0
    friend_ids = get_friends(access_token, user_id)
    friends = get_users(access_token, friend_ids)
    print(friends)


if __name__ == '__main__':
    main()
