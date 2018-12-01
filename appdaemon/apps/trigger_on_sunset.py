import appdaemon.plugins.hass.hassapi as hass
import datetime

class TriggerOnSunset(hass.Hass):

    def initialize(self):
        self.log("EveningLight Init")

        time_off = self.parse_time(self.args["off_time"])
        self.run_at_sunset(self.light_on, offset=int(self.args["sunset_offset"]))
        self.run_daily(self.light_off, time_off)

    def light_on(self, kwargs):
        self.turn_on(self.args["light"], brightness=self.args["brightness"])

    def light_off(self, kwargs):
        self.turn_off(self.args["light"])