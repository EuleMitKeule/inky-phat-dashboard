#! python3
# v1

# imports for getting data
import os
from json import loads
from time import sleep

import requests
from inky.auto import auto

# imports for inky
from PIL import Image, ImageDraw, ImageFont
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

inky_display = auto()

PATH = os.path.dirname(__file__)
fontpath = os.path.join(PATH, "MinecraftRegular.otf")
smallfont = ImageFont.truetype(fontpath, 22)
mediumfont = ImageFont.truetype(fontpath, 26)
bigfont = ImageFont.truetype(fontpath, 30)

# if whole house has a powercut, we need to wait until HA has rebooted before getting the sensor data
online = False

while not online:
    try:
        r = requests.get("http://192.168.0.104:4357")
        if r.status_code == 200:
            online = True
    except:
        sleep(1)
        continue

# HA is up and running, set up retries so we keep requesting if the first few don't work
retries = Retry(total=10, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retries)
http = requests.Session()
http.mount("http://", adapter)

headers = {
    "Authorization": "Bearer eyJhbGciOiJI...secrettoken...",
    "content-type": "application/json",
}

bindaystring = ""

while True:
    # get the sensor data for waste collection and extract the current state
    # the state is set from a value template in home assistant, so look in configuration.yaml if it needs changing
    response = http.get(
        "http://192.168.0.104:8123/api/states/sensor.waste_collection_schedule",
        headers=headers,
    )
    textdict = loads(response.text)

    if textdict["state"] == bindaystring:  # nothing has changed
        sleep(3600)
    else:  # there has been an update
        bindaystring = textdict["state"]

        bintype = bindaystring.split(" ")[0]  # will be Rubbish or Recycling
        binday = bindaystring.split(" ")[-1]  # will be days, today or tomorrow

        if bintype == "Rubbish":
            if binday == "days":
                inky_display.set_border(inky_display.BLACK)
                daystogo = bindaystring.split(" ")[-2]

                message = daystogo + " days"
                w, h = bigfont.getsize(message)
                x = (inky_display.WIDTH / 2) - (w / 2)
                y = (inky_display.HEIGHT / 2) - (h / 2)

                img = Image.open(os.path.join(PATH, "rubbish-days.png"))
                draw = ImageDraw.Draw(img)
                draw.text((x + 40, y - 14), "Rubbish", inky_display.BLACK, mediumfont)
                draw.text((x + 40, y + 14), message, inky_display.BLACK, bigfont)

            elif binday == "tomorrow":
                inky_display.set_border(inky_display.WHITE)

                message = "Tomorrow"
                w, h = mediumfont.getsize(message)
                x = (inky_display.WIDTH / 2) - (w / 2)
                y = (inky_display.HEIGHT / 2) - (h / 2)

                img = Image.open(os.path.join(PATH, "rubbish-tomorrow.png"))
                draw = ImageDraw.Draw(img)
                draw.text((x - 35, y - 14), "Rubbish", inky_display.WHITE, bigfont)
                draw.text((x - 35, y + 14), "Tomorrow", inky_display.WHITE, mediumfont)

            elif binday == "today":
                inky_display.set_border(inky_display.BLACK)

                message = "Today"
                w, h = bigfont.getsize(message)
                x = (inky_display.WIDTH / 2) - (w / 2)
                y = (inky_display.HEIGHT / 2) - (h / 2)

                img = Image.open(os.path.join(PATH, "rubbish-days.png"))
                draw = ImageDraw.Draw(img)
                draw.text((x + 25, y - 14), "Rubbish", inky_display.BLACK, bigfont)
                draw.text((x + 35, y + 14), message, inky_display.BLACK, bigfont)

            else:
                print("UNRECOGNISED BINSTRING", bindaystring)

        elif bintype == "Recycling":
            if binday == "days":
                inky_display.set_border(inky_display.RED)
                daystogo = bindaystring.split(" ")[-2]

                message = daystogo + " days"
                w, h = bigfont.getsize(message)
                x = (inky_display.WIDTH / 2) - (w / 2)
                y = (inky_display.HEIGHT / 2) - (h / 2)

                img = Image.open(os.path.join(PATH, "recycling-days.png"))
                draw = ImageDraw.Draw(img)
                draw.text((x + 50, y - 13), "Recycling", inky_display.RED, smallfont)
                draw.text((x + 50, y + 13), message, inky_display.RED, bigfont)

            elif binday == "tomorrow":
                inky_display.set_border(inky_display.WHITE)

                message = "Tomorrow"
                w, h = smallfont.getsize(message)
                x = (inky_display.WIDTH / 2) - (w / 2)
                y = (inky_display.HEIGHT / 2) - (h / 2)

                img = Image.open(os.path.join(PATH, "recycling-tomorrow.png"))
                draw = ImageDraw.Draw(img)
                draw.text((x - 42, y - 13), "Recycling", inky_display.WHITE, smallfont)
                draw.text((x - 42, y + 13), "Tomorrow", inky_display.WHITE, smallfont)

            elif binday == "today":
                inky_display.set_border(inky_display.RED)

                message = "Today"
                w, h = bigfont.getsize(message)
                x = (inky_display.WIDTH / 2) - (w / 2)
                y = (inky_display.HEIGHT / 2) - (h / 2)

                img = Image.open(os.path.join(PATH, "recycling-days.png"))
                draw = ImageDraw.Draw(img)
                draw.text((x + 48, y - 13), "Recycling", inky_display.RED, smallfont)
                draw.text((x + 53, y + 13), message, inky_display.RED, bigfont)
            else:
                print("UNRECOGNISED BINSTRING", bindaystring)
        else:  # neither rubbish nor recycling
            print("UNRECOGNISED BINSTRING", bindaystring)

        inky_display.set_image(img)
        inky_display.show()

        sleep(3600)
