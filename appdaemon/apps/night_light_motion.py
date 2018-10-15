import appdaemon.plugins.hass.hassapi as hass
import datetime

class NightLightMotion(hass.Hass):

    def initialize(self):
        self.log("NightLight Init")
    
        time_off = self.parse_time(self.args["constrain_end_time"])
        self.listen_state(self.motion, self.args["motion_sensor"])
        self.run_daily(self.light_off, time_off)
        self.log("NightLight: off time {} ".format(time_off))
    
    def motion(self, entity, attribute, old, new, kwargs):
        if new == "on" and old == "off":
            self.turn_on(self.args["light"], brightness=self.args["brightness"])
        elif new == "off" and old == "on":
            self.turn_off(self.args["light"])
        else:
            self.log("NightLight: Else trigger state old={}, state new={}".format(old, new))
    
    def light_off(self, kwargs):
        state = self.get_state(self.args["light"])
        if state == "on":
            self.turn_off(self.args["light"])