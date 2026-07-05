module.exports = {
  apps: [
    {
      name: 'eyeroll-recorder',
      script: 'recorder.js',
      cwd: __dirname,
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      restart_delay: 5000,
      max_restarts: 50,
      watch: false,
      env: {
        NODE_ENV: 'production'
      },
      out_file: './logs/recorder-out.log',
      error_file: './logs/recorder-error.log',
      time: true
    },
    {
      name: 'eyeroll-refresh',
      script: 'scripts/refresh-all.sh',
      cwd: __dirname,
      instances: 1,
      exec_mode: 'fork',
      autorestart: false,
      cron_restart: '0 */6 * * *',
      watch: false,
      out_file: './logs/refresh-out.log',
      error_file: './logs/refresh-error.log',
      time: true
    }
  ]
};
