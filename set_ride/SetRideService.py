import boto3
import os


def set_ride(user, route, stop, preset, agency):
    update_exp = 'SET #p = :b'
    user_table = boto3.resource('dynamodb', region_name='us-east-1').Table(os.environ['user_table'])
    response = user_table.update_item(
        Key={
            'user': user
        },
        UpdateExpression=update_exp,
        ExpressionAttributeNames={
            '#p': '%s-%s' % (agency, preset)
        },
        ExpressionAttributeValues={
            ':b': {'route': route, 'stop': stop}
        }
    )['ResponseMetadata']
    return response['HTTPStatusCode']

if __name__ == '__main__':
    os.environ['user_table'] = 'EZTransit_Users'
    set_ride('123', '7', '1174', '1', 'chicago-cta-bus')
