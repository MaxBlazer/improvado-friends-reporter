import requests
import json


def main():
    access_token = input('Enter access token: ')
    url = f'https://api.vk.com/method/friends.get?v=5.81&access_token={access_token}'
    response = requests.get(url)
    friend_ids = json.loads(response.text)['response']['items']
    print(friend_ids)


if __name__ == '__main__':
    main()
