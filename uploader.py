import argparse
from string import Template

import requests
from datetime import datetime, timezone, timedelta
from orbit_predictor.sources import get_predictor_from_tle_lines
from orbit_predictor.locations import Location


class Uploader:
    def __init__(self, args):
        self.slack_url = args.slackUrl
        self.location = Location("", latitude_deg=args.locationLat, longitude_deg=args.locationLng,
                                 elevation_m=args.locationElevation)
        self.satellite_tle_url = f'https://celestrak.com/satcat/tle.php?CATNR={args.satellite}'
        self.notification = args.notificationMsg

    def calculate_pass(self):
        # Calculate time to the next pass

        next_pass = self._get_satellite_tle()

        sat_in_utc = next_pass.aos.replace(tzinfo=timezone.utc)
        now_in_utc = datetime.now().astimezone(timezone.utc)
        time_difference = sat_in_utc - now_in_utc
        should_send_notification = timedelta(minutes=10) >= time_difference >= timedelta(minutes=9)

        if should_send_notification:
            self._send_notification(sat_in_utc, next_pass)

    def _get_satellite_tle(self):
        request = requests.get(self.satellite_tle_url)
        tle = request.content.decode('utf-8')
        lines = tle.split("\n")
        predictor = get_predictor_from_tle_lines(tuple(lines[1:3]))
        return predictor.get_next_pass(self.location)

    def _send_notification(self, sat_in_utc, next_pass):
        # Send notification to slack

        pass_hour = sat_in_utc.astimezone(datetime.now().tzinfo).strftime("%H:%m")
        pass_elevation = round(next_pass.max_elevation_deg, 2)

        message = Template(self.notification).substitute(pass_hour=pass_hour, pass_elevation=pass_elevation)
        self._send_message_to_slack(message)

    def _send_message_to_slack(self, msg):
        try:
            requests.post(self.slack_url, json={'text': msg})
        except Exception as e:
            print(e)


def main(args):
    uploader = Uploader(args)
    uploader.calculate_pass()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--satellite', '-s', help='Satellite NORAD ID', required=True)
    parser.add_argument('--locationLat', '-l', help='Location latitude (e.g. 52.29)', required=True, type=float)
    parser.add_argument('--locationLng', '-n', help='Location longitude (e.g. 18.67)', required=True, type=float)
    parser.add_argument('--locationElevation', '-e', help='Location elevation (m)', required=True, type=float)
    parser.add_argument('--slackUrl', '-u',
                        help='Slack incoming hook URL (e.g. https://hooks.slack.com/services/XXXXXXXX/YYYYY'
                             '/ZZZZZZZZZZZZZZZZ)',
                        required=True)
    parser.add_argument('--notificationMsg', '-m',
                        help='Notification message (e.g. "Next pass at $pass_hour with el: $pass_elevation°."',
                        required=True)
    return parser.parse_args()


main(parse_args())
