import boto3
import uuid

dyn_resource = boto3.resource('dynamodb')

class Users:

    def __init__(self):
        self.dyn_resource = dyn_resource
        self.table = None

    def create_table(self):
        self.table = self.dyn_resource.create_table(
            TableName='x23211946_EphUsers',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'},      
                {'AttributeName': 'eph_id', 'KeyType': 'RANGE'}   
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'eph_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
    
    def create_user(self, first_name, last_name, email, password):
        table_name = 'x23211946_EphUsers'
        table = self.dyn_resource.Table(table_name)
        
        id_value = str(uuid.uuid4())
        
        item = {
            'id': id_value,
            'eph_id': '#EP002',
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password
        }
        
        response = table.put_item(Item=item)

        return response

    
        
