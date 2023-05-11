FROM node:16-alpine

RUN npm install -g nodemon

WORKDIR /opt/app
COPY package.json package-lock.json /opt/app
RUN ci --dev
COPY . /opt/app/

EXPOSE 3000