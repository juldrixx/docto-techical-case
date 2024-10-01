# React Frontend

## Overview

This is a React-based frontend that interacts with a FastAPI backend. The frontend allows users to manage a list of todos and perform file uploads and downloads using an AWS S3 bucket. It communicates with the FastAPI backend via RESTful API endpoints.


## Installation

1. **Install dependencies**:

   ```bash
   npm install
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root of your project with the following content:

   ```
   REACT_APP_FASTAPI_URL=http://127.0.0.1:8000
   ```

   Modify the `REACT_APP_FASTAPI_URL` to point to your FastAPI backend URL (you may use `localhost` for development or your production URL).

3. **Run the application**:

   ```bash
   npm start
   ```

   The website will be available at `http://localhost:3000`.

## API Endpoints

This React frontend communicates with the following FastAPI endpoints:

- **GET /todos**: Retrieve a list of todos.
- **POST /todos**: Create a new todo.
- **DELETE /todos/{todo_id}**: Delete a specific todo by ID.
- **POST /objects**: Upload a file to the S3 bucket.
- **GET /objects**: List files in the S3 bucket.
- **GET /objects/{file_name}**: Download a specific file from the S3 bucket.
- **DELETE /objects/{file_name}**: Delete a specific file from the S3 bucket.

## Deployment

For production, build the project using:

```bash
npm run build
```

This will create a `build` directory with the static files to be deployed on a hosting platform like Netlify, Vercel, or any web server.
