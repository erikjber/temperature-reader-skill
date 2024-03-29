from mycroft import MycroftSkill, intent_file_handler
import urllib.request, json, time
from pathlib import Path

class TempereatureReader(MycroftSkill):
    def __init__(self):
        print("TemperatureReader init")
        MycroftSkill.__init__(self)
        self.homedir = str(Path.home())

    def stringify_temperature(self,temperature):
        res = "{:.1f}".format(temperature)
        # Remove trailing zeroes
        res = res.replace(".0","")
        return res

    @intent_file_handler('reader.tempereature.intent')
    def handle_reader_tempereature(self, message):
        print("Getting temperature")
        now = round(time.time()*1000)
        file_name = self.homedir+"/latestweather.json"
        with open(file_name,"r") as file:
            data = json.loads(file.read())
            # get the latest temperature
            if not data['temperatures']:
                self.speak_dialog('reader.nodata_atall')
                return 
            latest = data['temperatures'][0]
            # check they're no older than 15 minutes
            diff = now - latest['time']
            if diff > (15*60*1000):
                print("No temperature data in over 15 minutes.")
                self.speak_dialog('reader.nodata')
            else:
                output = {}
                output['latest_temp'] = self.stringify_temperature(latest['temp'])
                #print("It's " + str(latest['temp']) +" degrees outside.")
                # get min and max temperature
                max = -273
                min = 1000
                for d in data['temperatures']:
                    tmp  = d['temp']
                    if tmp < min:
                        min = tmp
                    if tmp > max:
                        max = tmp
                output['min_temp'] = self.stringify_temperature(min)
                output['max_temp'] = self.stringify_temperature(max)
                #print("In the last 24 hours the minimum was " + str(min) + " and the maximum " + str(max) +" degrees.")
                self.speak_dialog('reader.tempereature',output)

    @intent_file_handler('reader.mean.intent')
    def handle_mean_tempereature(self, message):
        print("Getting temperature")
        now = round(time.time()*1000)
        file_name = self.homedir+"/latest_dygn_weather.json"
        with open(file_name,"r") as file:
            data = json.loads(file.read())
            # get the latest temperature
            if not data['temperatures']:
                self.speak_dialog('reader.nodata_atall')
            else:
                output = {}
                sum = 0
                for d in data['temperatures']:
                    sum += d['temp']
                mean_temp = sum/len(data['temperatures'])
                output['mean_temp'] = self.stringify_temperature(mean_temp)
                self.speak_dialog('reader.mean',output)

def create_skill():
    return TempereatureReader()

