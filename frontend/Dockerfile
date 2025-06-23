FROM node:16-alpine

WORKDIR /app

# Add environment variable to handle React warnings
ENV CI=true
ENV WDS_SOCKET_PORT=0

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

# Use this for development
CMD ["npm", "start"]
