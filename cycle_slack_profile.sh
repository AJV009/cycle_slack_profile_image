if pgrep python | xargs ps | grep cycle_slack_profile > /dev/null
then
    echo "Slack profile updater already running"
    exit
else
    echo "Starting Slack profile updater in the background..."
    if [ -x "$(command -v mkvirtualenv)" ]; then
        if workon cycle_slack_profile > /dev/null; then
            workon cycle_slack_profile
        else
            mkvirtualenv cycle_slack_profile
            pip install -r ~/project/personal/cycle_slack_profile_image/requirements.txt
        fi
    fi
    python ~/project/personal/cycle_slack_profile_image/cycle_slack_profile.py &
fi
