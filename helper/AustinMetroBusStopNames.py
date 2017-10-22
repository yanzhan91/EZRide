import boto3
from boto3.dynamodb.conditions import Key
import logging as log


class AustinMetroBusStopNames:

    @staticmethod
    def get_stop_name(stop):
        try:
            user_table = boto3.resource('dynamodb', region_name='us-east-1').Table('AustinTransit_Stops')
            response = user_table.query(
                KeyConditionExpression=Key('stop_id').eq(int(stop)),
                Limit=1
            )
            return response['Items'][0]['stop_name']
        except Exception as e:
            log.info(e)
            return ''


if __name__ == "__main__":
    print AustinMetroBusStopNames().get_stop_name('1174')
