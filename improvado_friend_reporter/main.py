from improvado_friend_reporter.vk import VK
import csv

api_version = '5.81'


def dump_report(data, path='report', kind='csv'):
    data = sorted(data, key=lambda x: x['first_name'])

    fields = [
        'first_name',
        'last_name',
        'country',
        'city',
        'bdate',  # todo: iso
        'sex',
    ]

    # eliminate unnecessary fields
    data = [
        {
            field: value
            for field, value in entry.items()
            if field in fields
        }
        for entry in data
    ]

    for entry in data:
        try:
            entry['country'] = entry['country']['title']
            entry['city'] = entry['city']['title']
        except KeyError:
            pass

    if kind == 'csv':
        with open(f'{path}.csv', 'w') as file:
            writer = csv.DictWriter(file, fields)
            writer.writeheader()
            writer.writerows(data)
    else:
        raise ValueError('unknown format')


def main():
    access_token = input('Enter access token: ')
    user_id = input('Enter user id: ')
    api = VK(api_version, access_token)

    friend_ids = api.get_friends(user_id)['response']['items']
    print(friend_ids)
    friends = api.get_users(friend_ids, fields=['city', 'country', 'bdate', 'sex'])['response']
    print(friends)

    data = friends
    dump_report(data)


if __name__ == '__main__':
    main()
