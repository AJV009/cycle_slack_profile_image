if pgrep python3 | xargs ps | grep cycle_slack_profile > /dev/null
then
    echo "Slack profile updater already running"
    exit
else
    echo "Starting Slack profile updater in the background..."
    source ~/miniconda3/etc/profile.d/conda.sh;
    conda activate slackupdater; 
    python3 ~/project/personal/cycle_slack_profile_image/cycle_slack_profile.py &
fi
