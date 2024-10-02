# pylint: disable=redefined-outer-name
"""
Unit tests for the GCS actions.
"""
from unittest import mock
import pytest
from storage.actions import list_objects, put_object, delete_object, get_object

BUCKET_NAME = 'test-bucket'


@pytest.fixture(autouse=True)
def gcs_client(monkeypatch):
    """
    Fixture that sets up a mock Google Cloud Storage (GCS) client for testing.

    This fixture uses the 'unittest.mock' library to mock GCS services. It mocks the
    methods necessary for bucket and blob operations. The fixture is automatically
    applied to all test functions due to the 'autouse=True' parameter.

    Environment Variables Set:
        - OBJECT_BUCKET: The name of the GCS bucket to be used (set to 'test-bucket').
        - OBJECT_BUCKET_TYPE: The storage type (set to 'GCS').
    """
    monkeypatch.setenv('OBJECT_BUCKET', BUCKET_NAME)
    monkeypatch.setenv('OBJECT_BUCKET_TYPE', "GCS")

    # Mock the storage.Client class and its methods
    with mock.patch('google.cloud.storage.Client') as mock_client:
        mock_bucket = mock.Mock()
        mock_blob = mock.Mock()

        mock_client.return_value.bucket.return_value = mock_bucket
        mock_bucket.blob.return_value = mock_blob
        yield mock_client, mock_bucket, mock_blob


def test_list_objects_with_data(gcs_client):
    """
    Test listing objects in the GCS bucket when data is present.

    This test simulates two blobs in the mocked GCS bucket and verifies that 
    the list_objects function correctly returns their names and paths.

    Args:
        gcs_client (tuple): The mocked GCS client, bucket, and blob provided 
        by the gcs_client fixture.
    """
    _, mock_bucket, _ = gcs_client

    mock_blob_1 = mock.Mock()
    mock_blob_1.name = "testfile1.txt"

    mock_blob_2 = mock.Mock()
    mock_blob_2.name = "testfile2.txt"

    mock_bucket.list_blobs.return_value = [mock_blob_1, mock_blob_2]

    objects = list_objects()

    expected_objects = [
        {"name": "testfile1.txt", "path": "gs://test-bucket/testfile1.txt"},
        {"name": "testfile2.txt", "path": "gs://test-bucket/testfile2.txt"},
    ]

    assert objects == expected_objects


def test_list_objects_with_no_data(gcs_client):
    """
    Test listing objects in the GCS bucket when no data is present.

    This test verifies that the list_objects function returns an empty list 
    when there are no objects in the mocked GCS bucket.

    Args:
        gcs_client (tuple): The mocked GCS client, bucket, and blob provided 
        by the gcs_client fixture.
    """
    _, mock_bucket, _ = gcs_client
    mock_bucket.list_blobs.return_value = []

    objects = list_objects()

    assert objects == []


def test_put_object(gcs_client):
    """
    Test putting an object into the GCS bucket.

    This test uploads an object to the mocked GCS bucket using the 
    put_object function and verifies that the object has been successfully 
    uploaded by checking the GCS path of the object.

    Args:
        gcs_client (tuple): The mocked GCS client, bucket, and blob provided 
        by the gcs_client fixture.

    Asserts:
        - The GCS path of the uploaded object matches the expected path.
    """
    content = b"Hello, this is a test file."
    object_name = "myfile.txt"

    s3_path = put_object(object_name, content)

    _, _, mock_blob = gcs_client
    mock_blob.upload_from_string.assert_called_once_with(content)

    assert s3_path == f"gs://{BUCKET_NAME}/{object_name}"


def test_delete_object(gcs_client):
    """
    Test deleting an object from the GCS bucket.

    This test uploads an object to the mocked GCS bucket and then deletes 
    it using the delete_object function. It verifies that the object has 
    been removed by checking that the delete method is called on the blob.

    Args:
        gcs_client (tuple): The mocked GCS client, bucket, and blob provided 
        by the gcs_client fixture.

    Asserts:
        - The GCS path of the deleted object matches the expected path.
    """
    object_name = "testfile.txt"

    s3_path = delete_object(object_name)

    _, _, mock_blob = gcs_client
    mock_blob.delete.assert_called_once()

    assert s3_path == f"gs://{BUCKET_NAME}/{object_name}"


def test_get_object(gcs_client):
    """
    Test downloading an object from the GCS bucket.

    This test uploads an object to the mocked GCS bucket, then 
    downloads it using the get_object function. It verifies that 
    the downloaded content matches the expected content.

    Args:
        gcs_client (tuple): The mocked GCS client, bucket, and blob provided 
        by the gcs_client fixture.

    Asserts:
        - The downloaded content matches the expected content.
    """
    object_name = "testfile.txt"
    expected_content = b"Test file 1 content"

    _, _, mock_blob = gcs_client
    mock_blob.download_as_bytes.return_value = expected_content

    downloaded_content = get_object(object_name)

    assert downloaded_content == expected_content
