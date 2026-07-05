# Deployment guide: AWS Lightsail + PM2 + Nginx + GitHub Actions

This adds production deployment to the existing recorder/mirror project.

## Files added

- `ecosystem.config.js` - PM2 process definitions for the recorder and the periodic archive refresh.
- `.github/workflows/deploy.yml` - GitHub Actions workflow that deploys on every push to `main`.
- `deploy/nginx-eyeroll.conf` - Nginx server block serving the static mirror and recorder output.
- `deploy/lightsail-bootstrap.sh` - One-time server setup script for a fresh Lightsail Ubuntu instance.

## One-time server setup (Lightsail)

1. Create a Lightsail instance using the Ubuntu blueprint, attach a static IP.
2. SSH in, then upload or `curl` down `deploy/lightsail-bootstrap.sh`, or clone the repo first and run it from there:

```bash
chmod +x deploy/lightsail-bootstrap.sh
./deploy/lightsail-bootstrap.sh
```

This installs Node.js, ffmpeg, Nginx, and PM2, clones your repo, installs dependencies,
sets up the Nginx site, and starts both PM2 processes.

3. Point your domain's DNS (e.g. via Cloudflare) at the Lightsail static IP.
4. Edit `server_name` in `deploy/nginx-eyeroll.conf` on the server, reload Nginx, then run:

```bash
sudo certbot --nginx -d your-domain.com
```

## PM2 processes

`ecosystem.config.js` defines two apps:

- `eyeroll-recorder` - runs `recorder.js` continuously, auto-restarts on crash.
- `eyeroll-refresh` - runs `scripts/refresh-all.sh` on a cron schedule (every 6 hours) to rebuild `latest-frames.json`, MP4 archives, and `archive-index.json`.

Useful commands:

```bash
pm2 status
pm2 logs eyeroll-recorder
pm2 logs eyeroll-refresh
pm2 restart eyeroll-recorder
pm2 monit
```

## GitHub Actions auto-deploy

`.github/workflows/deploy.yml` runs on every push to `main`:

1. Checks out the repo.
2. SSHes into the Lightsail server.
3. Pulls the latest code, reinstalls dependencies, restarts PM2 processes.

### Required GitHub repo secrets

- `SERVER_HOST` - your Lightsail static IP or domain.
- `SERVER_USER` - the SSH username (e.g. `ubuntu`).
- `SSH_PRIVATE_KEY` - private key contents for a dedicated deploy key.

Generate a deploy key locally:

```bash
ssh-keygen -t rsa -b 4096 -C "github-actions" -f ./github-actions-deploy
```

Then:

- Append `github-actions-deploy.pub` to the server's `~/.ssh/authorized_keys`.
- Paste the contents of `github-actions-deploy` (private key) into the `SSH_PRIVATE_KEY` secret.

## Nginx

`deploy/nginx-eyeroll.conf` serves:

- The static mirror page and JSON indexes from `eyeroll-mirror/`.
- Recorded frames and archived MP4s from `eyeroll-recorder/` via an alias location.

Reload after any config change:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

## Cloudflare in front

Point your domain's DNS through Cloudflare (proxied) to the Lightsail static IP for CDN caching, TLS, and DDoS protection. No Cloudflare Workers or Browser Rendering are needed for this recorder/mirror architecture, since the workload is a persistent stateful process, not a stateless edge function.
