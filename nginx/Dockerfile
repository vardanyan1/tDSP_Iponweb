FROM nginx:stable-alpine

COPY conf/nginx.conf.template /etc/nginx/nginx.conf.template

CMD envsubst '${ALLOWED_HOST}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'
