from typing import List, Tuple, Union
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
    "units": "metric",
    "exclude": "current,minutely,daily"
}

weather_params_morby = {
    "lat": "56.5220654263617",
    "lon": "16.38096470028659",
    "appid": credentials["API_key"],  # Don't share this information on gitHub
    "units": "metric",
    "exclude": "current,minutely,daily"
}

weather_params_salem = {
    "lat": "59.199024748430205",
    "lon": "17.78318506684947",
    "appid": credentials["API_key"],  # Don't share this information on gitHub
    "units": "metric",
    "exclude": "current,minutely,daily"
}

weather_params_lund = {
    "lat": "55.71130220047952",
    "lon": "13.209363724861088",
    "appid": credentials["API_key"],  # Don't share this information on gitHub
    "units": "metric",
    "exclude": "current,minutely,daily"
}


def populate_weather_data(hours_forceast: List) -> Tuple[List[int], List[int], List[float], List[float], List[float]]:
    """
    Method for finding relevant data to present to the user
    """
    city_raining_hours = []
    condition_codes = []
    temperatures = []
    wind_speeds = []
    humidities = []
    for index, hour in enumerate(hours_forceast):
        condition_code = int(hour["weather"][0]["id"])
        temperature = float(hour["temp"])
        wind_speed = float(hour["wind_speed"])
        humidity = float(hour["humidity"])
        if condition_code < 700:
            # Supposed to be run at 7.am every day
            city_raining_hours.append(index + 7)
        condition_codes.append(condition_code)
        temperatures.append(temperature)
        wind_speeds.append(wind_speed)
        humidities.append(humidity)
    return (city_raining_hours, condition_codes, temperatures, wind_speeds, humidities)


# Get the weather data for wanted locations

# Hometown
hometown_response = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall", params=weather_params_hometown)
hometown_response.raise_for_status()
weather_data_hometown = hometown_response.json()
next_hours_hometown = weather_data_hometown["hourly"][:18]

hometown_raining_hours, hometown_condition_codes, hometown_temperatures, hometown_wind_speeds, hometown_humidities = populate_weather_data(
    next_hours_hometown)


# Morby
morby_response = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall", params=weather_params_morby)
morby_response.raise_for_status()
weather_data_morby = morby_response.json()
next_hours_morby = weather_data_morby["hourly"][:18]

morby_raining_hours, morby_condition_codes, morby_temperatures, morby_wind_speeds, morby_humidities = populate_weather_data(
    next_hours_morby)

# Salem
salem_response = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall", params=weather_params_salem)
salem_response.raise_for_status()
weather_data_salem = salem_response.json()
next_hours_salem = weather_data_salem["hourly"][:18]

salem_raining_hours, salem_condition_codes, salem_temperatures, salem_wind_speeds, salem_humidities = populate_weather_data(
    next_hours_salem)

# Lund
lund_response = requests.get(
    f"https://api.openweathermap.org/data/2.5/onecall", params=weather_params_lund)
lund_response.raise_for_status()
weather_data_lund = lund_response.json()
next_hours_lund = weather_data_lund["hourly"][:18]

lund_raining_hours, lund_condition_codes, lund_temperatures, lund_wind_speeds, lund_humidities = populate_weather_data(
    next_hours_lund)


def find_min_max_average(input_list: List[Union[int, float]]) -> Tuple[float, float, float]:
    """
    Method for finding the min, max and average from the input list
    """
    min_value = float(min(input_list))
    max_value = float(max(input_list))
    avg_value = round(float(sum(input_list) / len(input_list)), 2)
    return (min_value, max_value, avg_value)


def get_rain_message(raining_list: List[int], location: str) -> str:
    """
    Method for getting the rain message depending on if it is raining or not
    """
    if raining_list:
        rain_text = f"Godmorgon!\n\nIdag ser det ut att bli regn i {location}. Enligt prognosen kommer det att regna kl: "
        for time in raining_list:
            rain_text += str(time) + ":00, "
        rain_text = rain_text[:-2]
    else:
        rain_text = f"Godmorgon!\n\nDet kommer sannolikt att inte regna i {location} idag"
    rain_text += "."

    return rain_text


def get_temperature_message(temperatures: List[float]) -> str:
    """
    Method for getting the temperature information
    """
    min_temp, max_temp, avg_temp = find_min_max_average(temperatures)
    temp_text = f" Medeltemperaturen idag (7:00-22:00) kommer vara {avg_temp} grader. Dagens lagsta temperatur kommer vara {min_temp} medan den hogsta kommer vara {max_temp} grader."
    return temp_text


def get_wind_speed_message(wind_speeds: List[float]) -> str:
    """
    Method for getting information about the wind speed
    """
    _, max_speed, avg_speed = find_min_max_average(wind_speeds)
    wind_text = f" Vindhastighet kommer som max vara {max_speed}m/s men i medel: {avg_speed}m/s."
    return wind_text


def get_humidity_message(humidities: List[float]) -> str:
    """
    Method for getting information about the humidity
    """
    min_hum, max_hum, avg_hum = find_min_max_average(humidities)
    hum_text = f" Luftfuktigheten kommer vara mellan {min_hum}-{max_hum}% men i snitt vara {avg_hum}%."
    return hum_text


def get_codes_message(codes: List[int]) -> str:
    """
    Get hour for hour information about the upcomming weather
    """
    code_msg = " \n\nTimme for timme prognos nedan: \n"
    for hour, code in enumerate(codes):
        if code < 300:
            code_msg += f"Kl {hour+7}:00 - Thunderstorm\n"
        elif code < 400:
            code_msg += f"Kl {hour+7}:00 - Duggregn\n"
        elif code < 600:
            code_msg += f"Kl {hour+7}:00 - Regn\n"
        elif code < 700:
            code_msg += f"Kl {hour+7}:00 - Snow\n"
        elif code == 800:
            code_msg += f"Kl {hour+7}:00 - Klar himmel\n"
        else:
            code_msg += f"Kl {hour+7}:00 - Molnigt\n"
    return code_msg


def get_message(raining_list: List[int], condition_codes: List[int], temperatures: List[float], wind_speeds: List[float], humidities: List[float], location: str) -> str:
    """
    Method for generating the text with the weather information
    """
    email_text = f"Subject: Dagens prognos : {location}\n\n"
    email_text += get_rain_message(raining_list, location)
    email_text += get_temperature_message(temperatures[:-2])
    email_text += get_wind_speed_message(wind_speeds)
    email_text += get_humidity_message(humidities)
    email_text += get_codes_message(condition_codes)
    email_text += "\nHa en bra dag!\n/Pontus "
    return email_text


hometown_email = get_message(hometown_raining_hours, hometown_condition_codes,
                             hometown_temperatures, hometown_wind_speeds, hometown_humidities, "Farjestaden")
morby_email = get_message(morby_raining_hours, morby_condition_codes,
                          morby_temperatures, morby_wind_speeds, morby_humidities, "Morbylanga")
salem_email = get_message(salem_raining_hours, salem_condition_codes,
                          salem_temperatures, salem_wind_speeds, salem_humidities, "Salem")
lund_email = get_message(salem_raining_hours, salem_condition_codes,
                         salem_temperatures, salem_wind_speeds, salem_humidities, "Lund")


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
