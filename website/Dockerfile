# Use a smaller Node.js base image (Alpine variant)
FROM node:22.7.0-alpine AS build

# Set the working directory
WORKDIR /app

# Copy only the package.json and package-lock.json to reduce layer invalidation
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the project
RUN npm run build

# Use a smaller Nginx base image for the production stage
FROM nginx:alpine

# Copy the build output from the Node.js build stage to Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Copy a startup script
COPY docker-entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose the port that Nginx will listen on
EXPOSE 80

# Set entrypoint to use envsubst before nginx starts
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]