"""
This module provides utility functions for interacting with an S3 bucket 
using the `boto3` library.
"""
import os
import boto3


s3_client = boto3.client('s3')


def get_s3_bucket():
    """
    Retrieve the name of the S3 bucket from the environment variables.

    This function accesses the environment variable "S3_BUCKET" to get the 
    name of the S3 bucket that has been set in the environment. It is 
    useful for retrieving the bucket name in applications that interact 
    with AWS S3.

    Returns:
        str: The name of the S3 bucket, or None if the environment 
        variable is not set.
    """
    return os.getenv("S3_BUCKET")


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
    bucket_name = get_s3_bucket()
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
    bucket_name = get_s3_bucket()
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
    bucket_name = get_s3_bucket()
    s3_client.delete_object(
        Bucket=bucket_name,
        Key=name
    )

    return f"s3://{bucket_name}/{name}"
