# Use an official Nginx image as a parent image
FROM nginx:latest

# Copy the frontend content into the container at /usr/share/nginx/html
COPY . /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
