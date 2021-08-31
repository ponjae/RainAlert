from typing import List
from credentials import credentials
import requests
import smtplib

my_email = credentials["email"]
my_password = credentials["password"]

# Parameters for locating my hometown, where my grandparents and my uncle are living and where I am currently studying

weather_params_hometown = {
    "lat": "56.643258527395325",
    "lon": "16.474068515123577",
    "appid": credentials["API_key"],  # Don't share this information on gitHub
    "exclude": "current,minutely,daily"
}

weather_params_morby = {
    "lat": "56.5220654263617",
    "lon": "16.38096470028659",
    "appid": credentials["API_key"],  # Don't share this information on gitHub
    "exclude": "current,minutely,daily"
}

weather_params_salem = {
    "lat": "59.199024748430205",
    "lon": "17.78318506684947",
    "appid": credentials["API_key"],  # Don't share this information on gitHub
    "exclude": "current,minutely,daily"
}

weather_params_lund = {
    "lat": "55.71130220047952",
    "lon": "13.209363724861088",
    "appid": credentials["API_key"],  # Don't share this information on gitHub
    "exclude": "current,minutely,daily"
}

# Get the weather data for these three loactions

# Hometown
hometown_response = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall", params=weather_params_hometown)
hometown_response.raise_for_status()
weather_data_hometown = hometown_response.json()

raining_today_hometown = False
next_hours_hometown = weather_data_hometown["hourly"][:15]
raining_hours_hometown = []

for index, hour in enumerate(next_hours_hometown):
    condition_code = hour["weather"][0]["id"]
    if condition_code < 700:
        raining_today_hometown = True
        raining_hours_hometown.append(index + 7)  # Supposed to be run at 7:00

# Morby
morby_response = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall", params=weather_params_morby)
morby_response.raise_for_status()
weather_data_morby = morby_response.json()

raining_today_morby = False
next_hours_morby = weather_data_morby["hourly"][:15]
raining_hours_morby = []

for index, hour in enumerate(next_hours_morby):
    condition_code = hour["weather"][0]["id"]
    if condition_code < 700:
        raining_today_morby = True
        raining_hours_morby.append(index + 7)

# salem
salem_response = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall", params=weather_params_salem)
salem_response.raise_for_status()
weather_data_salem = salem_response.json()

raining_today_salem = False
next_hours_salem = weather_data_salem["hourly"][:15]
raining_hours_salem = []

for index, hour in enumerate(next_hours_salem):
    condition_code = hour["weather"][0]["id"]
    if condition_code < 700:
        raining_today_salem = True
        raining_hours_salem.append(index + 7)

# Lund
lund_response = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall", params=weather_params_lund)
lund_response.raise_for_status()
weather_data_lund = lund_response.json()

raining_today_lund = False
next_hours_lund = weather_data_lund["hourly"][:15]
raining_hours_lund = []

for index, hour in enumerate(next_hours_lund):
    condition_code = hour["weather"][0]["id"]
    if condition_code < 700:
        raining_today_lund = True
        raining_hours_lund.append(index + 7)


def get_message(is_raining: bool, raining_list: List[int], location: str) -> str:
    """
    Method for generating the text with the weather information
    """

    if is_raining:
        email_text = f"Subject:Regn idag!!!\n\nGodmorgon!\n\nIdag ser det ut att bli regn i {location}. Enligt prognosen kommer det att regna kl: "
        for time in raining_list:
            email_text += str(time) + ":00, "
        email_text = email_text[:-2]
        email_text += ".\n\nHa en bra dag och ta med ett paraply om du ska ut!\n/Pontus"
    else:
        email_text = f"Subject:Inget regn idag!!!\n\nGodmorgon!\n\nDet kommer sannolikt att inte regna i {location} idag, ha en fin dag!\n\n/Pontus"
    return email_text


hometown_email = get_message(
    raining_today_hometown, raining_today_hometown, "Farjestaden")
morby_email = get_message(
    raining_today_morby, raining_hours_morby, "Morbylanga")
salem_email = get_message(raining_today_salem, raining_hours_salem, "Salem")
lund_email = get_message(raining_today_lund, raining_hours_lund, "Lund")


with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=my_password)

    # Mail to persons in hometown
    connection.sendmail(from_addr=my_email,
                        to_addrs="johan.jaensson@electra.se", msg=hometown_email)
    connection.sendmail(from_addr=my_email,
                        to_addrs="marie.jaensson@olandsbank.se", msg=hometown_email)
    connection.sendmail(from_addr=my_email,
                        to_addrs="ponjae11@gmail.com", msg=hometown_email)

    # Mail to persons in morby
    connection.sendmail(from_addr=my_email,
                        to_addrs="mattiaspett@gmail.com", msg=morby_email)
    connection.sendmail(from_addr=my_email,
                        to_addrs="Mona.Jaensson@tele2.se", msg=morby_email)
    connection.sendmail(from_addr=my_email,
                        to_addrs="ponjae11@gmail.com", msg=morby_email)

    # Mail to persons in Salem
    connection.sendmail(from_addr=my_email,
                        to_addrs="antex7373@hotmail.com", msg=salem_email)
    connection.sendmail(from_addr=my_email,
                        to_addrs="ponjae11@gmail.com", msg=salem_email)

    # Mail to persons in Lund
    connection.sendmail(from_addr=my_email,
                        to_addrs="ponjae11@gmail.com", msg=lund_email)
    connection.sendmail(from_addr=my_email,
                        to_addrs="kajsa.j@icloud.com", msg=lund_email)
    connection.sendmail(from_addr=my_email,
                        to_addrs="ocke1998@gmail.com", msg=lund_email)
    connection.sendmail(from_addr=my_email,
                        to_addrs="idajohnren@gmail.com", msg=lund_email)
