FROM nginx:1.21.5-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY ./config/nginx.conf.* /etc/nginx/conf.d
ARG MODE
RUN echo $MODE
RUN mkdir /etc/nginx/templates
RUN if [ "$MODE" = "local" ]; then \
		mv /etc/nginx/conf.d/nginx.conf.local /etc/nginx/templates/nginx.conf.template; \
	elif [ "$MODE" = "production" ]; then \
		mv /etc/nginx/conf.d/nginx.conf.production /etc/nginx/templates/nginx.conf.template; \
	else \
		echo "Invalid MODE value: $MODE. Please specify either 'local' or 'production'." >&2; \
		exit 1; \
	fi
