FROM nginx:alpine

RUN rm /usr/share/nginx/html/*
COPY . /usr/share/nginx/html/

RUN rm /etc/nginx/conf.d/*
COPY proxy.conf /etc/nginx/conf.d/
