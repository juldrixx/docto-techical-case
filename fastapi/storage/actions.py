"""
This module provides utility functions for interacting with an S3 bucket 
using the `boto3` library.
"""
import os
import boto3
from google.cloud import storage


def get_s3_client():
    """
    Create and return an S3 client using the `boto3` library.

    This client is used to interact with the S3 service, allowing 
    operations such as uploading, downloading, listing, and deleting objects 
    from the bucket.

    Returns:
        boto3.S3.Client: A low-level client representing Amazon Simple Storage Service (S3).
    """
    return boto3.client('s3')


def get_gcs_client():
    """
    Create and return a Google Cloud Storage (GCS) client using the 
    `google.cloud.storage` library.

    This client is used to interact with GCS, allowing operations 
    such as uploading, downloading, listing, and deleting objects from 
    the bucket.

    Returns:
        google.cloud.storage.Client: A GCS client instance.
    """
    return storage.Client()


def get_bucket():
    """
    Retrieve the name of the bucket from the environment variables.

    This function accesses the environment variable "OBJECT_BUCKET" to get the 
    name of the bucket that has been set in the environment.

    Returns:
        str: The name of the bucket, or None if the environment 
        variable is not set.
    """
    return os.getenv("OBJECT_BUCKET")


def get_bucket_type():
    """
    Retrieve the type of the object storage system from environment variables.

    This function accesses the environment variable "OBJECT_BUCKET_TYPE" to determine 
    whether to use "S3" (default) or "GCS" for storage operations.

    Returns:
        str: The type of storage system, either "S3" or "GCS".
    """
    return os.getenv("OBJECT_BUCKET_TYPE", "S3")


def list_objects():
    """
    List all objects stored in the specified S3 bucket.

    **Returns**:
    - A list of dictionaries, where each dictionary represents an object 
      in the bucket with the following keys:
        - 'name': The object key (filename) in the S3 bucket.
        - 'path': The full S3 path to the object (s3://bucket_name/object_key).

    If no objects are found, an empty list is returned.

    **Example**:
    ```python
    objects = list_objects()
    for obj in objects:
        print(obj["name"], obj["path"])
    ```
    """
    bucket_name = get_bucket()
    bucket_type = get_bucket_type()

    if bucket_type == "GCS":
        gcs_client = get_gcs_client()
        bucket = gcs_client.bucket(bucket_name=bucket_name)
        blobs = bucket.list_blobs()
        return [{"name": blob.name, "path": f"gs://{bucket_name}/{blob.name}"} for blob in blobs]

    s3_client = get_s3_client()
    response = s3_client.list_objects(Bucket=bucket_name)
    if "Contents" not in response:
        return []

    return [{"name": obj['Key'], "path": f"s3://{bucket_name}/{obj['Key']}"}
            for obj in response['Contents']]


def put_object(name, content):
    """
    Upload an object (file) to the specified S3 bucket.

    **Args**:
    - name: The key (filename) to save the object under in the S3 bucket.
    - content: The file content or data to upload.

    **Returns**:
    - A string representing the full S3 path (s3://bucket_name/object_key) 
      where the file was uploaded.

    **Example**:
    ```python
    s3_path = put_object("myfile.txt", file_content)
    print(f"File uploaded to: {s3_path}")
    ```
    """
    bucket_name = get_bucket()
    bucket_type = get_bucket_type()

    if bucket_type == "GCS":
        gcs_client = get_gcs_client()
        bucket = gcs_client.bucket(bucket_name=bucket_name)
        blob = bucket.blob(name)
        blob.upload_from_string(content)
        return f"gs://{bucket_name}/{name}"

    s3_client = get_s3_client()
    s3_client.put_object(
        Bucket=bucket_name,
        Key=name,
        Body=content
    )

    return f"s3://{bucket_name}/{name}"


def delete_object(name):
    """
    Delete an object (file) from the specified S3 bucket.

    **Args**:
    - name: The key (filename) of the object to delete from the S3 bucket.

    **Returns**:
    - A string representing the full S3 path (s3://bucket_name/object_key) 
      of the deleted file.

    **Example**:
    ```python
    s3_path = delete_object("myfile.txt")
    print(f"File deleted from: {s3_path}")
    ```
    """
    bucket_name = get_bucket()
    bucket_type = get_bucket_type()

    if bucket_type == "GCS":
        gcs_client = get_gcs_client()
        bucket = gcs_client.bucket(bucket_name=bucket_name)
        blob = bucket.blob(name)
        blob.delete()
        return f"gs://{bucket_name}/{name}"

    s3_client = get_s3_client()
    s3_client.delete_object(
        Bucket=bucket_name,
        Key=name
    )

    return f"s3://{bucket_name}/{name}"


def get_object(name):
    """
    Retrieve an object (file) from the specified S3 bucket.

    **Args**:
    - name: The key (filename) of the object to retrieve from the S3 bucket.

    **Returns**:
    - bytes: The content of the object retrieved from the S3 bucket.

    **Raises**:
    - ClientError: If there is an issue with retrieving the object.

    **Example**:
    ```python
    file_content = get_object("myfile.txt")
    print(file_content)
    ```
    """
    bucket_name = get_bucket()
    bucket_type = get_bucket_type()

    if bucket_type == "GCS":
        gcs_client = get_gcs_client()
        bucket = gcs_client.bucket(bucket_name=bucket_name)
        blob = bucket.blob(name)
        return blob.download_as_bytes()

    s3_client = get_s3_client()

    response = s3_client.get_object(Bucket=bucket_name, Key=name)
    return response['Body'].read()
