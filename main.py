import os
import time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN"))

def lopped_profile_update(client):
  start_loop = False
  for filename in os.listdir('images'):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
      file_path = 'images/' + filename
      if not os.path.exists('.last_profile'):
        open('.last_profile', 'a').close()
        start_loop = True
      if start_loop:
        client.users_setPhoto(image=file_path)
        with open('.last_profile', 'w') as f:
          f.write(filename)
        time.sleep(3600)
      else:
        with open('.last_profile', 'r') as f:
          last_profile = f.read()
          if last_profile == filename:
            start_loop = True
          else:
            start_loop = False

if __name__ == "__main__":
  lopped_profile_update(app.client)
#   SocketModeHandler(app, os.environ["SLACK_BOT_USER_OAUTH_TOKEN"]).start()
