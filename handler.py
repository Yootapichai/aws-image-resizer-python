import boto3
import os
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import io

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

RESIZED_BUCKET = os.environ['RESIZED_BUCKET']
DYNAMO_TABLE = os.environ['DYNAMO_TABLE']
RESIZED_WIDTH = 800

def resize(event, context):
    try:
        s3_record = event['Records'][0]['s3']
        bucket = s3_record['bucket']['name']
        key = unquote_plus(s3_record['object']['key'])

        print(f"Processing image {key} from bucket {bucket}")

        file_ext = key.split('.')[-1].lower()
        if file_ext in ['jpg', 'jpeg']:
            output_format = 'JPEG'
            content_type = 'image/jpeg'
        elif file_ext == 'png':
            output_format = 'PNG'
            content_type = 'image/png'
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        # TODO: Add more

        file_byte_string = s3_client.get_object(Bucket=bucket, Key=key)['Body'].read()
        
        with Image.open(io.BytesIO(file_byte_string)) as image:
            width, height = image.size
            new_height = int((RESIZED_WIDTH / width) * height)
            
            image.thumbnail((RESIZED_WIDTH, new_height))
            
            if output_format == 'JPEG' and image.mode == 'RGBA':
                image = image.convert('RGB')

            buffer = io.BytesIO()
            image.save(buffer, format=output_format)
            buffer.seek(0)

        print(f"Successfully resized image, format: {output_format}")

        # "resized" prefix
        original_filename = key.split('/')[-1].split('.')[0]
        new_key = f"resized-{original_filename}.{file_ext}"

        s3_client.put_object(
            Bucket=RESIZED_BUCKET,
            Key=new_key,
            Body=buffer,
            ContentType=content_type
        )
        print(f"Successfully uploaded resized image to {RESIZED_BUCKET}")
        
        # DynamoDB
        table = dynamodb.Table(DYNAMO_TABLE)
        table.put_item(
            Item={
                'id': str(uuid.uuid4()),
                'originalFileName': key,
                'resizedFileName': new_key,
                'originalBucket': bucket,
                'resizedBucket': RESIZED_BUCKET,
                'createdAt': context.aws_request_id
            }
        )
        print(f"Successfully saved metadata to DynamoDB table {DYNAMO_TABLE}")

        return {'statusCode': 200, 'body': 'Image processed successfully!'}

    except Exception as e:
        print(f"Error processing image: {e}")
        return {'statusCode': 500, 'body': f'Error processing image: {str(e)}'}