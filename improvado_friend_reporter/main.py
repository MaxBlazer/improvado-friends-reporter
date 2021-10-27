import improvado_friend_reporter.reporter as reporter
from improvado_friend_reporter.vk import VK

api_version = '5.81'


def main():
    access_token = input('Enter access token: ')

    user_id = input('Enter user id: ')
    if not user_id:
        user_id = 0
        print(f"User id {user_id} is chosen")

    save_path = input('Enter file save path: ')
    if not save_path:
        save_path = 'report'
        print(f"File will be saved to '{save_path}' file")

    file_format = input('Choose file format (possible values: csv, tsv, json): ')
    if not file_format:
        file_format = 'csv'
        print(f"File format {file_format} is chosen")

    api = VK(api_version, access_token)

    response = api.get_friends(user_id)
    try:
        friend_ids = response['response']['items']
    except KeyError:
        print(response['error']['error_msg'])
        return

    response = api.get_users(friend_ids, fields=['city', 'country', 'bdate', 'sex'])
    try:
        friends = response['response']
    except KeyError:
        print(response['error']['error_msg'])
        return

    reporter.dump(friends, save_path, file_format)


if __name__ == '__main__':
    main()
