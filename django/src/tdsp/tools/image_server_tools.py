import base64
import imghdr
import json
import boto3
import uuid
import os
import environ

from django.core.files.base import ContentFile

env = environ.Env()


# TODO: revisit return types

def generate_image_name(decoded_img):
    ext = imghdr.what(None, h=decoded_img)

    # Generate a random 32-character name
    name = str(uuid.uuid4().hex)[:32]

    # Combine the name and extension to create the final image name
    image_name = f"{name}.{ext}"

    return image_name, ext


def get_content_type_from_ext(ext):
    content_type = 'application/octet-stream'

    if ext:
        if ext == 'jpeg':
            content_type = 'image/jpeg'
        elif ext == 'png':
            content_type = 'image/png'

    return content_type


# TODO: example unit test
# describe('get_content_type_from_ext', () => {
#     it('should return default content type if invalid extension was provided', () => {
# result = get_content_type_from_ext('asdasd')
# assert(res)
# })
# })

def save_image_to_minio(base64_image):
    # Decode the base64-encoded image
    decoded_img = base64.b64decode(base64_image)

    # create a ContentFile object from the decoded data
    name, ext = generate_image_name(decoded_img)
    content_type = get_content_type_from_ext(ext)
    img_file = ContentFile(decoded_img, name=name)

    # Credentials
    minio_user = os.environ.get('MINIO_ROOT_USER')
    minio_password = os.environ.get('MINIO_ROOT_PASSWORD')

    # Connect to the MinIO server
    s3 = boto3.client('s3',
                      endpoint_url='http://minio:9000',
                      aws_access_key_id=minio_user,
                      aws_secret_access_key=minio_password,
                      region_name='us-east-1',
                      )
    bucket_name = 'images'

    # Check if the bucket already exists
    if bucket_name not in [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]:
        # Create the bucket
        s3.create_bucket(Bucket=bucket_name)

        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": [
                        f"arn:aws:s3:::{bucket_name}/*"
                    ]
                }
            ]
        }
        s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))

    # Save the image to MinIO with public-read ACL
    s3.upload_fileobj(img_file, bucket_name, name,
                      ExtraArgs={
                          'ACL': 'public-read',
                          'ContentType': content_type,
                          'ContentDisposition': 'inline'
                      })
    if env.bool('DEBUG', default=False):
        # Generate a public URL for the image
        url = f'http://localhost:9000/{bucket_name}/{name}'
    else:
        url = f'http://localhost/{bucket_name}/{name}'

    # Return the URL to the Django application
    return url
