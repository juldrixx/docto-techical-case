#!/bin/sh

# Replace env vars in JavaScript files
echo "Injecting API URL into React app..."
find /usr/share/nginx/html/static/js -name "*.js" -exec sed -i "s|REACT_APP_FASTAPI_URL_PLACEHOLDER|$REACT_APP_FASTAPI_URL|g" {} \;

# Start nginx
nginx -g 'daemon off;'
