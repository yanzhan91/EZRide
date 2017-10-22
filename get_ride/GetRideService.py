import boto3
from boto3.dynamodb.conditions import Key
import os


def get_ride(user, preset, agency):
    user_table = boto3.resource('dynamodb').Table(os.environ['user_table'])
    response = user_table.query(
        KeyConditionExpression=Key('user').eq(user),
        Limit=1
    )

    try:
        user = response['Items'][0]
        data = user['%s-%s' % (agency, preset)]
        return data['route'], data['stop']
    except (KeyError, IndexError):
        return None, None


if __name__ == '__main__':
    os.environ['user_table'] = 'EZRide_Users'
    print get_ride('123', '1', 'chicago-cta-bus')
