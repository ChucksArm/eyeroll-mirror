lightsail_setup = '''#!/usr/bin/env bash
# One-time server bootstrap for AWS Lightsail (Ubuntu blueprint)
set -euo pipefail

echo "== Updating packages =="
sudo apt update && sudo apt upgrade -y

echo "== Installing Node.js (LTS) =="
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

echo "== Installing ffmpeg =="
sudo apt install -y ffmpeg

echo "== Installing Nginx =="
sudo apt install -y nginx

echo "== Installing PM2 globally =="
sudo npm install -g pm2

echo "== Cloning project =="
read -p "GitHub repo URL: " REPO_URL
git clone "$REPO_URL" ~/eyeroll-project
cd ~/eyeroll-project/eyeroll-recorder
npm install --production
mkdir -p logs

echo "== Setting up Nginx site =="
sudo cp deploy/nginx-eyeroll.conf /etc/nginx/sites-available/eyeroll
sudo ln -sf /etc/nginx/sites-available/eyeroll /etc/nginx/sites-enabled/eyeroll
sudo nginx -t && sudo systemctl reload nginx

echo "== Starting PM2 processes =="
pm2 startOrRestart ecosystem.config.js
pm2 save
pm2 startup systemd -u "$USER" --hp "$HOME" | tail -n 1 > /tmp/pm2_startup_cmd.sh
echo "Run the printed sudo command from /tmp/pm2_startup_cmd.sh to finish enabling PM2 on boot."

echo "== Done =="
echo "Edit deploy/nginx-eyeroll.conf server_name and rerun 'sudo nginx -t && sudo systemctl reload nginx' once your domain is pointed at this server."
echo "Then run: sudo certbot --nginx -d your-domain.com"
'''
with open('output/eyeroll-recorder/deploy/lightsail-bootstrap.sh', 'w') as f:
    f.write(lightsail_setup)
import os, stat
p = 'output/eyeroll-recorder/deploy/lightsail-bootstrap.sh'
os.chmod(p, os.stat(p).st_mode | stat.S_IEXEC)
print(len(lightsail_setup))