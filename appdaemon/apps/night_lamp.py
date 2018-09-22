import appdaemon.plugins.hass.hassapi as hass
import datetime

class NightLamp(hass.Hass):

  def initialize(self):
    time_off = self.parse_time(self.args["constrain_end_time"])
    self.log("time_off={}".format(time_off))
    self.listen_state(self.motion, self.args["motion_sensor"])
    self.run_daily(self.light_off, time_off)

  def motion(self, entity, attribute, old, new, kwargs):
    if new == "on" and old == "off":
      self.turn_on(self.args["light"], brightness=self.args["brightness"])
      self.log("if trigger: lamp on")
    elif new == "off" and old == "on":
      self.turn_off(self.args["light"])
      self.log("elif trigger: lamp off")
    else:
      self.log("Else trigger:")
      self.log("state old={}, state new={}".format(old, new))

  def light_off(self, kwargs):
    state = self.get_state(self.args["light"])
    self.log("light state={}".format(state))
    if state == "on":
      self.turn_off(self.args["light"])
      self.log("turn off lamp at constrain end time")
