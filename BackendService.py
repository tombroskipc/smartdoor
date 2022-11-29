import boto3
from constant import USER_TABBLE, ACCESS_HISTORY_TABLE
class BackendService:
    def __init__(self, database) -> None:
        self.database = database
        self.user_table = database.Table(USER_TABBLE)
        self.access_history_table = database.Table(ACCESS_HISTORY_TABLE)