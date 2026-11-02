FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY app.js dealership.js review.js ./
COPY data ./data
EXPOSE 3030
CMD ["node", "app.js"]
