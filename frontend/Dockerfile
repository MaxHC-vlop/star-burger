FROM node:16-alpine3.14

WORKDIR /opt/app

COPY package*.json ./
COPY /bundles-src ./bundles-src/

RUN npm ci --dev