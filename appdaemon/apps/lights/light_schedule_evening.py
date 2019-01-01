import appdaemon.plugins.hass.hassapi as hass
import datetime


class LightScheduleEvening(hass.Hass):
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
        self.log("LightSchedule Init")
        try:
            self.light = self.args["light"]
            time_off_week = datetime.time(22, 30, 0)
            time_off_weekend = datetime.time(23, 30, 0)
        except KeyError as e:
            self.log("Argument not found : {}".format(e), level="ERROR")
            return

        if "sunset_offset" in self.args:
            sunset_offset = self.args["sunset_offset"]
        else:
            sunset_offset = 0

        if "brightness" in self.args:
            self.brightness = self.args["brightness"]
        else:
            self.brightness = 0

        self.run_at_sunset(self.light_on, offset=int(sunset_offset))
        self.run_daily(self.light_off,
                       time_off_week,
                       constrain_days="mon,tue,wed,thu,sun")

        self.run_daily(self.light_off,
                       time_off_weekend,
                       constrain_days="fri,sat")
        self.log("light:{}, brightness:{}, offset:{}\n"
                 .format(self.friendly_name(self.light), self.brightness, sunset_offset))

    def light_on(self, kwargs):
        if self.brightness:
            self.turn_on(self.light, brightness=self.brightness)
        else:
            self.turn_on(self.light)
        self.log("Line: __line__, Function: __function__, Message: Turn on {} with brightness {}\n"
                 .format(self.friendly_name(self.light), self.brightness))

    def light_off(self, kwargs):
        self.turn_off(self.light)
        self.log("Line: __line__, Function: __function__, Message: Turn off {}\n"
                 .format(self.friendly_name(self.light)))
