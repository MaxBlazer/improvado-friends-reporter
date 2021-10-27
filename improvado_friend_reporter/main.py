from improvado_friend_reporter.vk import VK

api_version = '5.81'


def main():
    access_token = input('Enter access token: ')
    api = VK(api_version, access_token)

    user_id = 0
    friend_ids = api.get_friends(user_id)['response']['items']
    print(friend_ids)
    friends = api.get_users(friend_ids)
    print(friends)


if __name__ == '__main__':
    main()
