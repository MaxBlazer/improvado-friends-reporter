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
        'bdate',
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
        # replace with human-readable country/city
        try:
            entry['country'] = entry['country']['title']
            entry['city'] = entry['city']['title']
        except KeyError:
            pass

        # drop dates that aren't full, then transform to iso
        try:
            date_tuple = entry['bdate'].split('.')
        except KeyError:
            continue

        if len(date_tuple) == 3:
            entry['bdate'] = '.'.join(reversed(date_tuple))
        else:
            del entry['bdate']

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

    friend_ids = api.get_friends(user_id)['response']['items']
    friends = api.get_users(friend_ids, fields=['city', 'country', 'bdate', 'sex'])['response']

    dump_report(friends, save_path, file_format)


if __name__ == '__main__':
    main()
