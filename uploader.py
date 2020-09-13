import requests
from datetime import datetime, timezone, timedelta
from orbit_predictor.sources import get_predictor_from_tle_lines
from orbit_predictor.locations import Location

slack_url = ''

gliwice = Location("GLIWICE", latitude_deg=50.29761, longitude_deg=18.67658, elevation_m=219)
satellite_tle_url = ''


def get_satellite_tle():
    request = requests.get(satellite_tle_url)
    tle = request.content.decode('utf-8')
    lines = tle.split("\n")
    predictor = get_predictor_from_tle_lines(tuple(lines[1:3]))
    next_pass = predictor.get_next_pass(gliwice)

    sat_in_utc = next_pass.aos.replace(tzinfo=timezone.utc)
    now_in_utc = datetime.now().astimezone(timezone.utc)
    time_difference = sat_in_utc - now_in_utc
    should_send_notification = timedelta(minutes=10) >= time_difference >= timedelta(minutes=9)
    print(sat_in_utc - now_in_utc)
    print(should_send_notification)

    format_next_pass = sat_in_utc.astimezone(datetime.now().tzinfo).strftime("%H:%m")
    # format_next_pass = sat_in_utc.strftime("%H:%m")

    notification = f""
    print(notification)
    # send_message_to_slack(notification)


def send_message_to_slack(msg):
    try:
        requests.post(slack_url, json={'text': msg})
    except Exception as e:
        print(e)


# send_message_to_slack('test script')

get_satellite_tle()
