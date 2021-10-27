import csv
import json

fields = [
        'first_name',
        'last_name',
        'country',
        'city',
        'bdate',
        'sex',
    ]


def dump(data, path='report', kind='csv'):
    data = _process(data)

    if kind == 'csv':
        _dump_csv(data, path, fields)
    elif kind == 'tsv':
        _dump_tsv(data, path, fields)
    elif kind == 'json':
        _dump_json(data, path)
    else:
        raise ValueError('unknown format')


def _process(data):
    data = sorted(data, key=lambda x: x['first_name'])

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

    return data


def _dump_csv(data, path, fields):
    with open(f'{path}.csv', 'w') as file:
        writer = csv.DictWriter(file, fields)
        writer.writeheader()
        writer.writerows(data)


def _dump_tsv(data, path, fields):
    with open(f'{path}.tsv', 'w') as file:
        writer = csv.DictWriter(file, fields, dialect='excel-tab')
        writer.writeheader()
        writer.writerows(data)


def _dump_json(data, path):
    with open(f'{path}.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False)
