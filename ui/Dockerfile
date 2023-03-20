# Use Node.js 14 as the base image
FROM node:14-alpine

# Set the working directory to /app
WORKDIR /ui

# Copy the package.json and package-lock.json files to the working directory
COPY package*.json ./

# Install dependencies
RUN apk add yarn && yarn install

# Copy the rest of the application files to the working directory
COPY . .

# Expose port 3000 for the app to run on
EXPOSE 3000

# Start the app
CMD ["yarn", "start"]
