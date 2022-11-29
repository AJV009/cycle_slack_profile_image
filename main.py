import os
import time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN"))

def lopped_profile_update(client):
  # Store loop status
  start_loop = False
  # Store first image path 
  first_image = ""
  # Loop through all images in the images folder
  for filename in os.listdir('images'):
    # check weather images end with jpg/png/jpeg
    suffix = ("jpg", "png", "jpeg")
    if filename.endswith(suffix):
      # Mkae it full path
      file_path = 'images/' + filename
      # Check if first image is set, if not set it
      # If we loop the second time and we see that first image is set, we know that we have looped through all images
      # So we can reset last_profile and start the loop again
      if first_image == "":
        first_image = file_path
      elif first_image == file_path:
        start_loop = True
        if os.path.exists('.last_profile'):
          os.remove('.last_profile')
      # Check if we have a last_profile file, if not set it
      # and begin the loop
      if not os.path.exists('.last_profile'):
        open('.last_profile', 'a').close()
        start_loop = True
      # If start_loop is true, we can update the profile
      if start_loop:
        client.users_setPhoto(image=file_path)
        with open('.last_profile', 'w') as f:
          f.write(filename)
        # Wait for an hour before updating the profile again
        time.sleep(3600)
      # Else check if the last_profile file is the same as the current image
      # If it is, we can start the loop
      # if not, we can skip the image
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
