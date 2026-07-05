nginx_conf = '''# Eyeroll Tenderloin mirror - Nginx server block
# Save as /etc/nginx/sites-available/eyeroll and symlink into sites-enabled

server {
    listen 80;
    listen [::]:80;
    server_name your-domain.com;

    root /home/ubuntu/eyeroll-project/output/eyeroll-mirror;
    index tenderloin-mirror-static.html;

    location / {
        try_files $uri $uri/ =404;
        add_header Cache-Control "no-store";
    }

    location /latest-frames.json {
        add_header Cache-Control "no-store";
    }

    location /archive-index.json {
        add_header Cache-Control "no-store";
    }

    # Serve recorded frames and archived MP4s from the recorder folder
    location /eyeroll-recorder/ {
        alias /home/ubuntu/eyeroll-project/output/eyeroll-recorder/;
        autoindex off;
    }

    gzip on;
    gzip_types application/json text/html text/css application/javascript;
}
'''
with open('output/eyeroll-recorder/deploy/nginx-eyeroll.conf', 'w') as f:
    f.write(nginx_conf)
print(len(nginx_conf))