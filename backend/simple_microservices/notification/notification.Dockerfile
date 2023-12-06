FROM node:slim
WORKDIR /app
COPY . /app
RUN npm install
EXPOSE 5005
CMD node index.js