deploy_yml = '''name: Deploy Eyeroll Recorder

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Deploy to Lightsail via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            set -e
            cd /home/${{ secrets.SERVER_USER }}/eyeroll-project
            git pull origin main
            cd eyeroll-recorder
            npm install --production
            mkdir -p logs
            pm2 startOrRestart ecosystem.config.js
            pm2 save
'''
with open('output/eyeroll-recorder/.github/workflows/deploy.yml', 'w') as f:
    f.write(deploy_yml)
print(len(deploy_yml))