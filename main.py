import requests
from twilio.rest import Client
import os

# Title : Rain Alert Project that sends SMS
# Author : Harriet Fiagbor
# Date : 9/3/21 9:23 PM

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_ACCOUNT_AUTH_TOKEN")

ACCRA_LAT = 5.564540
ACCRA_LONG = -0.225710
OWM_API_KEY = os.getenv("OWM_API_KEY")
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")

parameters = {
    "lat": ACCRA_LAT,
    "lon": ACCRA_LONG,
    "appid": OWM_API_KEY,
    "exclude": "current,daily,minutely",
}

will_rain = False

response = requests.get(OWM_ENDPOINT, params=parameters)
response.raise_for_status()
weather_data = response.json()["hourly"][:12]
for hour in weather_data:
    condition_code = hour["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="It's going to rain today. Bring an umbrella ☔",
        from_='+14157543958',
        to=PHONE_NUMBER
    )
    print(message.status)

