# FastAPI

## Overview

This project is a **FastAPI** application designed to handle CRUD operations for a Todo list, and interact with an AWS S3 bucket for file upload, download, and management. The project uses **SQLAlchemy** for database interactions and **Pydantic** for data validation and serialization. Additionally, **AWS S3** operations are integrated for handling file uploads and downloads.

## Key Features

- RESTful API for managing Todos.
- Integration with AWS S3 for file storage.
- Automatic generation of interactive API documentation (Swagger UI and ReDoc).
- CORS support for interaction with front-end applications (e.g., React).
- High performance using asynchronous request handling.

## Technologies Used

- **FastAPI**: For creating the API.
- **SQLAlchemy**: For database ORM.
- **Pydantic**: For data validation.
- **Uvicorn**: ASGI server for serving the FastAPI application.
- **AWS S3**: For file storage.
- **Botocore**: For handling S3-related exceptions.
- **CORS Middleware**: For enabling cross-origin resource sharing.

## Installation

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file with the necessary environment variables:

   ```
   TESTING=false
   FASTAPI_ROOT_PATH=<your-root-path>
   ```

   Optionally, set up MySQL credentials and AWS credentials for S3 operations:

   ```
   MYSQL_USER=<your-mysql-user>
   MYSQL_PASSWORD=<your-mysql-password>
   MYSQL_HOST=<your-mysql-host>
   MYSQL_PORT=<your-mysql-port>
   MYSQL_DB=<your-mysql-db>
   AWS_ACCESS_KEY_ID=<your-access-key-id>
   AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
   S3_BUCKET=<your-s3-bucket-name>
   ```

3. **Run the application**:

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Todos Endpoints

- **GET /todos**: Retrieve a paginated list of todo items.
- **POST /todos**: Create a new todo item.
- **DELETE /todos/{todo_id}**: Delete a specific todo item by ID.

### S3 File Endpoints

- **POST /objects**: Upload a file to the S3 bucket.
- **GET /objects**: List all files in the S3 bucket.
- **DELETE /objects/{file_name}**: Delete a specific file from the S3 bucket.
- **GET /objects/{file_name}**: Download a file from the S3 bucket.

### Example Requests

#### Get Todos:
```bash
curl -X 'GET' 'http://127.0.0.1:8000/todos' -H 'accept: application/json'
```

#### Upload a File:
```bash
curl -X 'POST' 'http://127.0.0.1:8000/objects' -H 'accept: application/json' -F 'file=@/path/to/your/file'
```

## Testing

To run tests, ensure that the `TESTING` environment variable is set to `true`, and run:

```bash
TESTING=true pytest
```
