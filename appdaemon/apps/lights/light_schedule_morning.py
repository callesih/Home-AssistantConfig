import appdaemon.plugins.hass.hassapi as hass
import datetime

class LightScheduleMorning(hass.Hass):
    """

    Exampel configuration:
      module: light_schedule_evening
      class: LightScheduleEvening
      light: light.tradfri_bulb_e14_w_opch_400lm
      brightness: 147
      sunset_offset: +450

    Arguments:
      light: light enity to control
      brightness: brightness level (optional)
      susnet_offset: time in secons to offset action (optional)
    """

    def initialize(self):
        self.log("LightScheduleMorning init")
        self.triggered = False

        try:
            self.light = self.args["light"]
            self.motion_sensor = self.args["motion_sensor"]
            self.activate_time = self.args["activate_time"]
            self.deactivate_time = self.args["deactivate_time"]
        except KeyError as e:
            self.log("Argument not found : {}".format(e), level="ERROR")
            return

        if "brightness" in self.args:
            self.brightness = self.args["brightness"]
        else:
            self.brightness = 0

        time_off = self.parse_time(self.deactivate_time)
        time_off = (datetime.datetime.combine(datetime.date(1, 1, 1), time_off) + datetime.timedelta(minutes=2)).time()

        self.listen_state(self.motion,
                          self.motion_sensor,
                          new = "on",
                          constrain_start_time=self.activate_time,
                          constrain_end_time=self.deactivate_time)

        self.run_daily(self.light_off, time_off)
        self.log("light:{}, motion_sensor:{}, activate_time:{}, deactivate_time:{}, brightness:{}, time_off:{}\n"\
                 .format(self.friendly_name(self.light),
                 self.friendly_name(self.motion_sensor),
                 self.activate_time,
                 self.deactivate_time,
                 self.brightness, time_off))

    def motion(self, entity, attribute, old, new, kwargs):
        self.state = self.get_state(self.light)

        if self.state == "off" and self.triggered == False:
            if self.brightness:
                self.turn_on(self.light, brightness=self.brightness)
            else:
                self.turn_on(self.light)
            self.triggered = True
            self.log("\nLine: __line__, Function: __function__, \nMessage: Turn on {} with brightness {} \n"\
                     .format(self.friendly_name(self.light), self.brightness))

    def light_off(self, kwargs):
        self.turn_off(self.light)
        self.triggered = False