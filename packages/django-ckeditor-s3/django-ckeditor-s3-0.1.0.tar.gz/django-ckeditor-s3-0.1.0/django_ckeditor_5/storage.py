from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticEditStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    default_acl = "public-read"