# Build stage
FROM node:18-alpine AS build
ENV REACT_APP_API_URL=http://13.233.108.196:8000/api
ENV API_BASE_FALLBACK=http://13.233.108.196:8000/api
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

# Runtime stage
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
