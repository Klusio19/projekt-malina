import requests as rq
import json
import urllib3
import light_specific_vars
import time


def change_power():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disable warning about insecure connection
    header = light_specific_vars.header
    light_url = light_specific_vars.light_url
    payload_on = json.dumps({
        "on": {
            "on": True
        }
    })

    payload_off = json.dumps({
        "on": {
            "on": False
        }
    })
    a = rq.get(url=light_url, headers=header, verify=False)
    response_json = a.json()
    light_on = response_json['data'][0]['on']['on']
    if light_on:
        rq.put(light_url, headers=header, data=payload_off, verify=False)
    else:
        rq.put(light_url, headers=header, data=payload_on, verify=False)


def change_brightness(level):
    if level > 100:
        level = 100
    elif level < 0:
        level = 0

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disable warning about insecure connection
    header = light_specific_vars.header
    light_url = light_specific_vars.light_url
    payload = json.dumps({
        "dimming": {
            "brightness": level
        }
    })
    rq.put(url=light_url, headers=header, data=payload, verify=False)


def change_color(x, y):
    r = rq.put(light_specific_vars.light_url, headers=light_specific_vars.header,
               json={
                   "color": {
                       "xy": {
                           "x": x,
                           "y": y
                       }
                   }
               }, verify=False)
    # print(it)
    if (r.status_code == 200) or (r.status_code == 207):
        pass
    else:
        print(r.status_code)
