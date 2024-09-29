version: '3.8'

services:
  fastapi:
    image: ghcr.io/juldrixx/docto-technical-case-fastapi:latest
    environment:
      - FASTAPI_ROOT_PATH=${fastapi_path}
    ports:
      - "8000:8000"

  website:
    image: ghcr.io/juldrixx/docto-technical-case-website:latest
    environment:
      - REACT_APP_FASTAPI_URL=http://${fastapi_dns}${fastapi_path}
    ports:
      - "80:80"