import appdaemon.plugins.hass.hassapi as hass
import datetime

class NightLight(hass.Hass):

  def initialize(self):
    self.log("NightLight Init")

    time_off = self.parse_time(self.args["constrain_end_time"])
    self.listen_state(self.motion, self.args["motion_sensor"])
    self.run_daily(self.light_off, time_off)

  def motion(self, entity, attribute, old, new, kwargs):

    if new == "on" and old == "off":
      self.turn_on(self.args["light1"], brightness=self.args["brightness1"])
      livingroom_lamp = self.update_livingroom_lamp()
      if livingroom_lamp:
        self.turn_on(self.args["light2"], brightness=self.args["brightness2"])
    elif new == "off" and old == "on":
      self.turn_off(self.args["light1"])
      if self.now_is_between("23:30:00", "05:35:00"):
        state2 = self.get_state(self.args["light2"])
        if state2 == "on":
          self.turn_off(self.args["light2"])
    else:
      self.log("Else trigger:")
      self.log("state old={}, state new={}".format(old, new))

  def light_off(self, kwargs):
    state1 = self.get_state(self.args["light1"])
    state2 = self.get_state(self.args["light2"])
    if state1 == "on":
      self.turn_off(self.args["light1"])
    if state2 == "on":
      self.turn_off(self.args["light2"])

  def update_livingroom_lamp(self):
    self.log("Update_livingroom_lamp trigger:")
    state = self.get_state("input_boolean.guests_mode")
    if self.now_is_between("23:30:00", "05:30:00"):
      if state == "off":
        return True
    return False

