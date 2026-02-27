FROM node:20-alpine AS build

WORKDIR /app

COPY frontend/package.json /app/frontend/package.json
COPY frontend/package-lock.json /app/frontend/package-lock.json

RUN npm config set registry https://registry.npmmirror.com && \
    if [ -f /app/frontend/package-lock.json ]; then \
      cd /app/frontend && npm ci; \
    else \
      cd /app/frontend && npm install; \
    fi

COPY frontend /app/frontend

ARG VITE_OTP_ADMIN_NAME
ENV VITE_OTP_ADMIN_NAME=$VITE_OTP_ADMIN_NAME

RUN cd /app/frontend && npm run build

FROM nginx:1.25-alpine

COPY docker/frontend/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/frontend/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
