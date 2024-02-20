FROM node:18-alpine as BUILD_IMAGE
WORKDIR /app/react-app

COPY . .
RUN npm install
RUN npm install typescript
RUN npm run build
CMD ["npm", "run", "preview"]
