import appdaemon.plugins.hass.hassapi as hass
import datetime

class NightLightMotion(hass.Hass):

    def initialize(self):
        self.log("Initializing NightLightMotion...")

        time_off = self.parse_time(self.args["deactivate_time"])
        time_off = (datetime.datetime.combine(datetime.date(1, 1, 1), time_off) + datetime.timedelta(minutes=2)).time()
        
        self.listen_state(self.motion,
                          self.args["motion_sensor"],
                          constrain_start_time = self.args["activate_time"],
                          constrain_end_time = self.args["deactivate_time"])

        self.run_daily(self.light_off, time_off)
        self.log("NightLightMotion: off time {}".format(time_off))
        self.log("Done initializing NightLightMotion")
    
    def motion(self, entity, attribute, old, new, kwargs):
        if new == "on" and old == "off":
            if self.args["brightness"]:
                self.turn_on(self.args["light"], brightness=self.args["brightness"])
            else:
                self.turn_on(self.args["light"])
            self.log("NightLight Turn on lamp")
        elif new == "off" and old == "on":
            self.turn_off(self.args["light"])
        else:
            self.log("NightLight: Else trigger state old={}, state new={}".format(old, new))
    
    def light_off(self, kwargs):
        state = self.get_state(self.args["light"])
        self.log("NightLight Turn lamp of constrain_end_time, state lamp = {}".format(state))
        if state == "on":
            self.turn_off(self.args["light"])