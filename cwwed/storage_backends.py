import os
import boto3
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from named_storms.utils import create_directory


class S3ObjectStorage(S3Boto3Storage):
    """
    AWS S3 Storage backend
    """

    def __init__(self, *args, **kwargs):
        self.location = self._get_location()  # ie. "local", "dev" or "" when in production
        self.default_acl = 'private'
        self.access_key = settings.CWWED_ARCHIVES_ACCESS_KEY_ID
        self.secret_key = settings.CWWED_ARCHIVES_SECRET_ACCESS_KEY
        self.bucket_name = settings.AWS_ARCHIVE_BUCKET_NAME
        self.custom_domain = '%s.s3.amazonaws.com' % settings.AWS_ARCHIVE_BUCKET_NAME
        self.auto_create_bucket = True

        super().__init__(*args, **kwargs)

    @staticmethod
    def _get_location():
        """
        Defines a "prefix" path in storage.  Empty if we're deploying to production
        """
        if settings.DEPLOY_STAGE == settings.DEPLOY_STAGE_PROD:
            return ''
        return settings.DEPLOY_STAGE

    def _get_s3_client(self):
        # create s3 client
        return boto3.resource(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )

    def download_directory(self, obj_directory_path, file_system_path):
        # create the s3 instance
        s3 = boto3.resource('s3')
        s3_bucket = s3.Bucket(self.bucket_name)

        # create directory output directory on file system
        create_directory(file_system_path)

        # download each object that matches the `obj_directory_path` prefix
        for obj in s3_bucket.objects.all():
            if obj.key.startswith(obj_directory_path):
                self.download_file(obj.key, os.path.join(file_system_path, os.path.basename(obj.key)))

    def download_file(self, obj_path, file_system_path):
        # create directory then download to file system path
        create_directory(os.path.dirname(file_system_path))
        s3 = self._get_s3_client()
        s3.Bucket(self.bucket_name).download_file(obj_path, file_system_path)

    def copy_within_storage(self, source: str, destination: str):
        """
        Copies an S3 object to another location within the same bucket
        """

        # delete any existing version if it exists
        if self.exists(destination):
            self.delete(destination)

        # create absolute references to account for the default_storage "location" (prefix)
        source_absolute = self.path(source)
        destination_absolute = self.path(destination)

        s3 = self._get_s3_client()
        copy_source = {
            'Bucket': settings.AWS_ARCHIVE_BUCKET_NAME,
            'Key': source_absolute,
        }
        s3.meta.client.copy(copy_source, self.bucket_name, destination_absolute)

    def path(self, path):
        """
        Include the default_storage "location" (prefix), i.e "local", "dev", "test" etc.  Will be empty when in production
        """
        return os.path.join(self.location, path)

    def storage_url(self, path):
        return os.path.join(
            's3://',
            self.bucket_name,
            self.location,
            path,
        )


class S3StaticStorage(S3Boto3Storage):
    """
    AWS S3 Storage backend for static assets
    """

    def __init__(self, *args, **kwargs):
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        self.custom_domain = '%s.s3.amazonaws.com' % settings.AWS_STORAGE_BUCKET_NAME
        self.auto_create_bucket = True
        self.file_overwrite = False
        self.gzip = True

        super().__init__(*args, **kwargs)
