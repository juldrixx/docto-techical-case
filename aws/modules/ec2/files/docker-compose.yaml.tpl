version: '3.8'

services:
  fastapi:
    image: ghcr.io/juldrixx/docto-technical-case-fastapi:latest
    environment:
      - FASTAPI_ROOT_PATH=${fastapi_path}
      - MYSQL_USER=${mysql_user}
      - MYSQL_PASSWORD=${mysql_password}
      - MYSQL_HOST=${mysql_host}
      - MYSQL_PORT=${mysql_port}
      - MYSQL_DB=${mysql_db}
      - OBJECT_BUCKET=${s3_bucket}
      - OBJECT_BUCKET_TYPE=S3
    ports:
      - "8000:8000"

  website:
    image: ghcr.io/juldrixx/docto-technical-case-website:latest
    environment:
      - REACT_APP_FASTAPI_URL=http://${fastapi_dns}${fastapi_path}
    ports:
      - "80:80"