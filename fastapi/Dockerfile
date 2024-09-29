# Use a smaller base image (Alpine)
FROM python:3.12-alpine AS builder

# Set working directory
WORKDIR /app

# Install build dependencies to compile any necessary wheels (only if required)
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev

# Copy only requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final stage to copy dependencies and only necessary files
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]