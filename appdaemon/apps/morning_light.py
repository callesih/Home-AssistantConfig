import appdaemon.plugins.hass.hassapi as hass
import datetime

class MorningLight(hass.Hass):

    def initialize(self):
        self.log("MorningLight init")

        time_off = self.parse_time(self.args["deactivate_time"])
        time_off = (datetime.datetime.combine(datetime.date(1, 1, 1), time_off) + datetime.timedelta(minutes=2)).time()
        self.listen_state(self.motion,
                          self.args["motion_sensor"],
                          new = "on",
                          constrain_start_time = self.args["activate_time"],
                          constrain_end_time = self.args["deactivate_time"])

        self.run_daily(self.light_off, time_off)
        self.log("MorningLight: off time {} ".format(time_off))

    def motion(self, entity, attribute, old, new, kwargs):
        self.state = self.get_state(self.args["light"])

        if self.state == "off":
            self.turn_on(self.args["light"], brightness=self.args["brightness"])

    def light_off(self, kwargs):
        self.turn_off(self.args["light"])
