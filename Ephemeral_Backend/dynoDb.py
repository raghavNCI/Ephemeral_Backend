class CreateUserTable:

    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table = None

    def create_table(self):
        self.table = self.dyn_resource.create_table(
            TableName='x23211946_sample',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'},       # Partition key
                {'AttributeName': 'eph_id', 'KeyType': 'RANGE'}   # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'N'},
                {'AttributeName': 'eph_id', 'AttributeType': 'S'},
                # {'AttributeName': 'email', 'AttributeType': 'S'},
                # {'AttributeName': 'password', 'AttributeType': 'B'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
