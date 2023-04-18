module.exports = {
  apps : [{
    name   : "cycle_slack_profile_image",
    script : "main.sh",
    watch: true,
    max_memory_restart: "500M",
    autorestart: true,
    max_restarts: 10,
  }]
}
