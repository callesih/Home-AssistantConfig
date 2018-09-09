import appdaemon.plugins.hass.hassapi as hass

class EveningLamp(hass.Hass):

  def initialize(self):
    self.run_at_sunset(self.light_on, offset=int(self.args["sunset_offset"])
    self.run_daily(self.light_off, self.args["off_time"]

  def light_on(self, kwargs):
    self.turn_on(self.args["light"], brightness=self.args["brightness"])

  def light_off(self, kwargs):
    self.turn_off(self.args["light"])

