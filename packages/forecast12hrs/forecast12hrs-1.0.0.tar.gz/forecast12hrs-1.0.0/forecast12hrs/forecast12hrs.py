import requests


# API key: 41c799ec83d9e4b396f9b2b0a5636f1c

class Weather:
    """ Create a Weather object getting an apikey as input
    and either a city name or lat and lon coordinates

    Package use example:

    # Create a weather object using a city name:
    # The api key below is not guranateed to work.
    # Create your own api key from https://openweathermao.org.
    # And wait a couple of hours for the api key to be acyivated.
    
    # Using the city name :
     >>> weather1 = weather(apikey ="41c799ec83d9e4b396f9b2b0a5636f1c", city = "chennai")

    # Using lat and lon coordinates :
     >>> weather2 = weather(apikey ="41c799ec83d9e4b396f9b2b0a5636f1c",lat = 3.2,lon= 4.1)

    # Get a complete weather report for next 12 hours :
     >>> weather1.next_12hours()
    
    """

    def __init__(self,apikey,city=None,lat=None,lon=None):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("provide either city or lat and lon arguments")

        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])

    def next_12hour(self):
        return self.data['list'][:4]

    def next_12hour_simplified(self):
        simple_data = []
        for dicty in self.data['list'][:4]:
            simple_data.append((dicty['dt_txt'],dicty['main']['temp'],dicty['weather'][0]['description']))
        return simple_data


