FROM node:18-alpine as BUILD_IMAGE
WORKDIR /app
ARG MODE=local
ARG SERVER_NAME
ENV PROTOCOL=http
RUN if [ "$MODE" != "local" ]; then PROTOCOL=https; fi
RUN echo "VITE_API_URL=$PROTOCOL://$SERVER_NAME" >> .env
COPY ./package*.json .
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "run", "preview"]
