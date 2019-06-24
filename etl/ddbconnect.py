# Template for connecting to AWS DynamoDB

import boto3

class DDBConnect:
    def __init__(self, table):
        session = boto3.Session(profile_name='',
                                region_name='us-west-2')
        self.ddb_resource = session.resource('dynamodb')
        self.ddb_client = session.client('dynamodb')
        self.ddb_table = self.ddb_resource.Table(table)

    def getTables(self):
        return self.ddb_client.list_tables()

    def batchPutData(self, data):
        with self.ddb_table.batch_writer() as batch:
            for item in data:
                batch.put_item(Item=item)