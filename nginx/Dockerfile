FROM nginx

RUN mkdir /etc/nginx/sites-available

COPY app.conf /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/app.conf /etc/nginx/conf.d/
