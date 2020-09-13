# satellite pass slack reminder 

Small python script to upload information about a passing satellite to Slack via [incoming webhooks](https://api.slack.com/messaging/webhooks) ~10 minutes before the pass.
 
### requirements
- python > 3.5.0
- packages from `requirements.txt`

### usage

```
pip install -r requirements.txt
```

```
python uploader.py [-h] --satellite SATELLITE --locationLat LOCATIONLAT --locationLng LOCATIONLNG --locationElevation LOCATIONELEVATION --slackUrl SLACKURL --notificationMsg NOTIFICATIONMSG

arguments
  -h, --help            show this help message and exit
  --satellite SATELLITE, -s SATELLITE
                        Satellite NORAD ID (its TLE has to be available at the address 'https://celestrak.com/satcat/tle.php?CATNR={satellite}')
  --locationLat LOCATIONLAT, -l LOCATIONLAT
                        Location latitude (e.g. 52.29)
  --locationLng LOCATIONLNG, -n LOCATIONLNG
                        Location longitude (e.g. 18.67)
  --locationElevation LOCATIONELEVATION, -e LOCATIONELEVATION
                        Location elevation (m)
  --slackUrl SLACKURL, -u SLACKURL
                        Slack incoming hook URL (e.g. https://hooks.slack.com/services/XXXXXXXX/YYYYY/ZZZZZZZZZZZZZZZZ)
  --notificationMsg NOTIFICATIONMSG, -m NOTIFICATIONMSG
                        Notification message (e.g. "Next pass at $pass_hour with el: $pass_elevation°."

```

The assumed usage scenario is to setup a cron **every 1 minute** running the above script with proper arguments.

Example cron:

```
* * * * * python uploader.py --satellite 12345 --locationLat 51.123 --locationLng 18.123 --locationElevation 200 --slackUrl https://hooks.slack.com/services/XXXXXX/YYYYYYYYYY/ZZZZZZZZZZZ --notificationMsg "The satellite is passing in ~10 minutes ($pass_hour) with elevation: $pass_elevation°."
```
