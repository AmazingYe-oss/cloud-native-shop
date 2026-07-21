FROM nginx:1.25-alpine
COPY services/frontend/index.html /usr/share/nginx/html/
COPY services/frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80 || exit 1
CMD ["nginx", "-g", "daemon off;"]