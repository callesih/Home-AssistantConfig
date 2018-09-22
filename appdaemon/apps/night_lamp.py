import appdaemon.plugins.hass.hassapi as hass

class NightLamp(hass.Hass):

  def initialize(self):
    self.listen_state(self.motion, self.args["motion_sensor"], new = "on")

  def motion(self, entity, attribute, old, new, kwargs):
    #if self.now_is_between("sunset + 00:30:00", "sunrise - 00:15:00"):
    self.turn_on(self.args["light"], brightness=self.args["brightness"])
    self.run_in(self.light_off, 30)
    #self.set_state(self.args["motion_sensor"], state=off)

  def light_off(self, kwargs):
    self.turn_off(self.args["light"])
