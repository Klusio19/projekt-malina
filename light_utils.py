import requests as rq
import json
import light_specific_vars


def check_response(response: rq.Response):
    if (response.status_code != 200) and (response.status_code != 207):
        print(f'There is something wrong with the API call! Status code: {response.status_code}')


def powered_on():
    header = light_specific_vars.header
    light_url = light_specific_vars.light_url
    r = rq.get(url=light_url, headers=header, verify=False)
    check_response(r)
    response_json = r.json()
    light_on = response_json['data'][0]['on']['on']
    if light_on:
        return True
    else:
        return False


def change_power():
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
    if powered_on():
        r = rq.put(light_url, headers=header, data=payload_off, verify=False)
        check_response(r)
    else:
        r = rq.put(light_url, headers=header, data=payload_on, verify=False)
        check_response(r)


def change_brightness(level):
    if level > 100:
        level = 100
    elif level < 0:
        level = 0

    header = light_specific_vars.header
    light_url = light_specific_vars.light_url
    payload = json.dumps({
        "dimming": {
            "brightness": level
        }
    })
    r = rq.put(url=light_url, headers=header, data=payload, verify=False)
    check_response(r)


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
    check_response(r)
