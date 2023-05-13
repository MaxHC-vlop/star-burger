FROM node:16-alpine3.14

WORKDIR /opt/app

COPY package*.json /opt/app/

RUN npm ci --only=production && npm cache clean --force

COPY . .

EXPOSE 3000