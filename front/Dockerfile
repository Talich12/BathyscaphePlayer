FROM node:alpine as builder
WORKDIR /frontend/
EXPOSE 8080
COPY package*.json .

RUN npm install

COPY . . 

RUN npm run build

FROM devforth/spa-to-http:latest
COPY --from=builder /frontend/dist/ .