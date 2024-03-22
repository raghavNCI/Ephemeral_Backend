import boto3
from botocore.exceptions import ClientError

class DisplayPic:
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        
    def createDPBucket(self):
        try:
            self.s3_client.create_bucket(Bucket='x23211946-ephdpbucket', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
            return {'successful': True, 'message': 'Bucket created'}
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyExists':
                return {'successful': False, 'message': 'Bucket already exists'}
            else:
                return {'successful': False, 'message': str(e)}
                
    def get_presigned_url(self, eph_id, expiration=3600):
        object_key = str(eph_id + "/displayPic.jpg")
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': 'x23211946-ephdpbucket', 'Key': object_key},
                ExpiresIn=expiration
            )
            return {'successful': True, 'message': response}
        except ClientError as e:
            return {'successful': False, 'message': str(e)}
    
    def upload_dp_to_s3(self, image_data, eph_id):
        
        content_type = 'image/jpeg'
        object_key = str(eph_id + "/displayPic.jpg")
        
        try:
            response = self.s3_client.put_object(
                Body=image_data,
                Bucket='x23211946-ephdpbucket',
                Key=object_key,
                ContentType = content_type
            )
            return {'successful': True, 'message': 'Image uploaded successfully', 'response': response}
        except ClientError as e:
            return {'successful': False, 'message': f'Error uploading image to S3: {str(e)}'}

