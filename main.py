import os
import time
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import random
load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN"))
pic_array = [pic for pic in os.listdir(os.environ.get('BASE_PATH')+'images') if pic.endswith(("jpg", "png", "jpeg"))]
pic_array.sort()

def last_profile(pic='', change_mode='w'):
  lp_path = os.environ.get('BASE_PATH')+'.last_profile'
  # write
  if change_mode == 'w':
    with open(lp_path, 'w') as f:
      f.write(pic)
  # create new and write
  elif change_mode == 'n':
    if os.path.exists(lp_path):
      os.remove(lp_path)
    with open(lp_path, 'w') as f:
      f.write(pic)
  # read current_pic
  elif change_mode == 'r':
    if os.path.exists(lp_path):
      with open(lp_path, 'r') as f:
        pic = f.read()
        if pic in pic_array:
          return pic
        else:
          last_profile(pic_array[0], 'n')
          return pic_array[0]
    else:
      last_profile(pic_array[0], 'n')
      return pic_array[0]

def update_details(client, pic):
  display_name = os.environ.get('DISPLAY_NAME')
  display_name = "".join( random.choice([k.upper(), k.lower() ]) for k in display_name )
  client.users_profile_set(profile={"display_name": display_name})
  file_path = os.environ.get('BASE_PATH')+'images/'+pic
  if os.path.exists(file_path):
    client.users_setPhoto(image=file_path)

def loop_profile_update(client):
  start_loop = False
  sleep_time = int(os.environ.get('SLEEP_TIME'))
  while (True):
    for idx, pic in enumerate(pic_array):
      if last_profile(change_mode='r') == pic:
        start_loop = True
      else:
        start_loop = False
      if start_loop:
        update_details(client, pic)
        if pic == pic_array[-1]:
          last_profile(pic_array[0], 'n')
        else:
          last_profile(pic_array[idx+1], 'w')
        time.sleep(sleep_time)

if __name__ == "__main__":
  loop_profile_update(app.client)
