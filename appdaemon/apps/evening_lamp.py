import appdaemon.plugins.hass.hassapi as hass
import datetime

class EveningLamp(hass.Hass):

  def initialize(self):
#    time_off = self.parse_time(self.args["off_time"])
    time_on = datetime.time(20, 00, 0)
    time_off = datetime.time(23, 00, 00)
#    self.run_at_sunset(self.light_on, offset=300)
    self.run_daily(self.light_on, time_on)
    self.run_daily(self.light_off, time_off)

  def light_on(self, kwargs):
    self.turn_on(self.args["light"], brightness=self.args["brightness"])

  def light_off(self, kwargs):
    self.turn_off(self.args["light"])

