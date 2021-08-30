from credentials import credentials
import requests
import smtplib

my_email = credentials["email"]
my_password = credentials["password"]

weather_params = {
    "lat": "56.649921",
    "lon": "16.473579",
    "appid": credentials["API_key"],  # Don't share this information on gitHub
    "exclude": "current,minutely,daily"
}


response = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall", params=weather_params)
response.raise_for_status()
weather_data = response.json()

raining_today = False
next_fourteen = weather_data["hourly"][:14]
raining_hours = 0

for hour in next_fourteen:
    condition_code = hour["weather"][0]["id"]
    if condition_code < 700:
        raining_today = True
        raining_hours += 1


with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=my_email, password=my_password)
    if raining_today:
        connection.sendmail(from_addr=my_email,
                            to_addrs="johan.jaensson@electra.se", msg=f"Subject:Regn idag!!!\n\nDet kommer sannolikt att regna i {raining_hours} av de kommande 14 timmarna, ta med ett paraply om du ska ut!")
        connection.sendmail(from_addr=my_email,
                            to_addrs="marie.jaensson@olandsbank.se", msg=f"Subject:Regn idag!!!\n\nDet kommer sannolikt att regna i {raining_hours} av de kommande 14 timmarna, ta med ett paraply om du ska ut!")
        connection.sendmail(from_addr=my_email,
                            to_addrs="mattiaspett@gmail.com", msg=f"Subject:Regn idag!!!\n\nDet kommer sannolikt att regna i {raining_hours} av de kommande 14 timmarna, ta med ett paraply om du ska ut!")
        connection.sendmail(from_addr=my_email,
                            to_addrs="ponjae11@gmail.com", msg=f"Subject:Regn idag!!!\n\nDet kommer sannolikt att regna i {raining_hours} av de kommande 14 timmarna, ta med ett paraply om du ska ut!")
    else:
        connection.sendmail(from_addr=my_email,
                            to_addrs="johan.jaensson@electra.se", msg=f"Subject:Inget regn idag\n\nDet kommer sannolikt att inte regna inom de kommande 14 timmarna, ha en bra dag!")
        connection.sendmail(from_addr=my_email,
                            to_addrs="marie.jaensson@olandsbank.se", msg=f"Subject:Inget regn idag\n\nDet kommer sannolikt att inte regna inom de kommande 14 timmarna, ha en bra dag!")
        connection.sendmail(from_addr=my_email,
                            to_addrs="mattiaspett@gmail.com", msg=f"Subject:Inget regn idag\n\nDet kommer sannolikt att inte regna inom de kommande 14 timmarna, ha en bra dag!")
        connection.sendmail(from_addr=my_email,
                            to_addrs="ponjae11@gmail.com", msg=f"Subject:Inget regn idag\n\nDet kommer sannolikt att inte regna inom de kommande 14 timmarna, ha en bra dag!")
