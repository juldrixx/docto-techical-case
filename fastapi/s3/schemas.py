"""
This module defines Pydantic models used for validating and serializing 
S3 data.
"""
from typing import List, Optional
from pydantic import BaseModel


class FileInfo(BaseModel):
    """
    Model representing basic information about a file stored in S3.

    Attributes:
    - name: The name of the file (S3 object key).
    - path: The full S3 path to the file.
    """
    name: str
    path: str


class UploadResponse(BaseModel):
    """
    Model representing the response after successfully uploading a file 
    to S3.

    Attributes:
    - message: A success message indicating the file was uploaded.
    """
    message: str


class ListFilesResponse(BaseModel):
    """
    Model representing the response from listing files in an S3 bucket.

    Attributes:
    - files: A list of FileInfo objects containing information about 
      the files stored in the bucket. If no files exist, this will be an 
      empty list.
    """
    files: Optional[List[FileInfo]] = []


class DeleteResponse(BaseModel):
    """
    Model representing the response after successfully deleting a file 
    from S3.

    Attributes:
    - message: A success message indicating the file was deleted.
    """
    message: str
