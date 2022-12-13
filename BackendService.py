import boto3
from constant import USER_TABBLE, ACCESS_HISTORY_TABLE
from botocore.config import Config


class BackendService:
    def __init__(self, database) -> None:
        self.database = boto3.resource('dynamodb')
        self.user_table = database.Table(USER_TABBLE)
        self.access_history_table = database.Table(ACCESS_HISTORY_TABLE)
        self.aws_config = Config(
            region_name='ap-southeast-1',
            signature_version='v4',
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )

    def get_user(self, username: str):
        query_key = {
            'username': username
        }
        response = self.user_table.get_item(Key=query_key)

        return response['Item']
