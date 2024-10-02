# pylint: disable=redefined-outer-name
"""
Unit tests for the S3 actions.
"""
import pytest
import boto3
from moto import mock_aws
from storage.actions import list_objects, put_object, delete_object, get_object

BUCKET_NAME = 'test-bucket'


@pytest.fixture(autouse=True)
def s3_client(monkeypatch):
    """
    Fixture that sets up a mock AWS S3 client for testing.

    This fixture uses the 'moto' library to mock AWS services. It creates a 
    temporary S3 bucket and sets the necessary environment variables to 
    simulate AWS credentials and region settings. The fixture is 
    automatically applied to all test functions due to the 'autouse=True' 
    parameter.

    Environment Variables Set:
        - AWS_ACCESS_KEY_ID: Mock access key for AWS (set to 'test').
        - AWS_SECRET_ACCESS_KEY: Mock secret key for AWS (set to 'test').
        - AWS_DEFAULT_REGION: Mock region for AWS (set to 'us-east-1').
        - OBJECT_BUCKET: The name of the S3 bucket to be used (set to 
          'test-bucket').

    Yields:
        boto3.resource: A boto3 resource representing the mocked S3 service, 
        allowing for S3 operations like creating buckets and putting objects.
    """
    with mock_aws():
        monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'test')
        monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'test')
        monkeypatch.setenv('AWS_DEFAULT_REGION', 'us-east-1')
        monkeypatch.setenv('OBJECT_BUCKET', BUCKET_NAME)
        monkeypatch.setenv('OBJECT_BUCKET_TYPE', "S3")
        s3 = boto3.resource('s3')
        s3.create_bucket(Bucket=BUCKET_NAME)
        yield s3


def test_list_objects_with_data(s3_client):
    """
    Test listing objects in the S3 bucket when data is present.

    This test puts two objects into the mocked S3 bucket and verifies that 
    the list_objects function correctly returns their names and paths.

    Args:
        s3_client (boto3.resource): The mocked S3 resource provided by the 
        s3_client fixture.
    """
    s3_client.Bucket(BUCKET_NAME).put_object(
        Key="testfile1.txt", Body=b"Test file 1 content")
    s3_client.Bucket(BUCKET_NAME).put_object(
        Key="testfile2.txt", Body=b"Test file 2 content")

    objects = list_objects()

    expected_objects = [
        {"name": "testfile1.txt", "path": "s3://test-bucket/testfile1.txt"},
        {"name": "testfile2.txt", "path": "s3://test-bucket/testfile2.txt"},
    ]

    assert objects == expected_objects


def test_list_objects_with_no_data():
    """
    Test listing objects in the S3 bucket when no data is present.

    This test verifies that the list_objects function returns an empty list 
    when there are no objects in the mocked S3 bucket.
    """
    objects = list_objects()
    assert objects == []


def test_put_object():
    """
    Test putting an object into the S3 bucket.

    This test uploads an object to the mocked S3 bucket using the 
    put_object function and verifies that the object has been successfully 
    uploaded by checking its name and path in the list of uploaded objects.

    Asserts:
        - The number of uploaded objects is 1.
        - The name of the uploaded object matches the expected object name.
        - The path of the uploaded object matches the expected S3 path.
    """
    content = b"Hello, this is a test file."
    object_name = "myfile.txt"

    s3_path = put_object(object_name, content)

    uploaded_objects = list_objects()
    assert len(uploaded_objects) == 1
    assert uploaded_objects[0]["name"] == object_name
    assert uploaded_objects[0]["path"] == s3_path


def test_delete_object(s3_client):
    """
    Test deleting an object from the S3 bucket.

    This test uploads an object to the mocked S3 bucket and then deletes 
    it using the delete_object function. It verifies that the object has 
    been removed by checking that the list of uploaded objects is empty 
    after the deletion.

    Args:
        s3_client (boto3.resource): The mocked S3 resource provided by the 
        s3_client fixture.

    Asserts:
        - The number of uploaded objects after deletion is 0.
        - The S3 path of the deleted object matches the expected path.
    """
    s3_client.Bucket(BUCKET_NAME).put_object(
        Key="testfile.txt", Body=b"Test file 1 content")

    s3_path = delete_object("testfile.txt")

    uploaded_objects = list_objects()
    assert len(uploaded_objects) == 0
    assert s3_path == "s3://test-bucket/testfile.txt"


def test_get_object(s3_client):
    """
    Test downloading an object from the S3 bucket.

    This test uploads an object to the mocked S3 bucket, then 
    downloads it using the get_object function. It verifies that 
    the downloaded content matches the original content.

    Args:
        s3_client (boto3.resource): The mocked S3 resource provided by the 
        s3_client fixture.

    Asserts:
        - The downloaded content matches the original content uploaded.
    """
    s3_client.Bucket(BUCKET_NAME).put_object(
        Key="testfile.txt", Body=b"Test file 1 content")

    downloaded_content = get_object("testfile.txt")

    assert downloaded_content == b"Test file 1 content"
