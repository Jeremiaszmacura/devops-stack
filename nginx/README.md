# Nginx

Nginx can be used to many different purposes, such as serving static files, load balancing, and acting as a reverse proxy for other web servers.

## Nginx Exporter

The Nginx Exporter is a Prometheus exporter that collects metrics from Nginx. It can be used to monitor the performance and health of your Nginx server. Key metrics include:
- Request rates
- Response times
- Active connections
- Server status and healts
- HTTP response codes
etc.

### How it works

1. The exporter connects to NGINX's /nginx_status endpoint via http://nginx-service/nginx_status
2. It scrapes metrics from this status page
3. Converts the data to Prometheus format
4. Exposes the metrics on port 9113 for Prometheus to collect
