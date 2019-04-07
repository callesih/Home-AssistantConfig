import appdaemon.plugins.hass.hassapi as hass
import datetime

from typing import Callable

#
# House mode app
#
# Args:
#


class HouseModes(hass.Hass):

    def initialize(self):
        motion_sensor = self.args["motion_sensor"]
        activate_time = self.args["activate_time"]
        deactivate_time = self.args["deactivate_time"]
        sunset_offset = self.args["sunset_offset"]
        sunrise_offset = self.args["sunrise_offset"]
        night_time = self.args["night_time"]
        night_time = self.parse_time(night_time)

        self.listen_state(self.morgon,
                          motion_sensor,
                          new="on",
                          constrain_start_time=activate_time,
                          constrain_end_time=deactivate_time)

        self.run_at_sunset(self.kvall, offset=int(sunset_offset))
        self.run_at_sunrise(self.dag, offset=int(sunrise_offset))

        self.run_daily(self.natt, night_time)

    def morgon(self, entity, attribute, old, new, kwargs):
        current_mode = self.get_current_mode()
        if current_mode == "Natt":
            self.select_option("input_select.house_modes", "Morgon")
            self.debug_log()

    def natt(self, kwargs):
        current_mode = self.get_current_mode()
        if current_mode == "Dag" or current_mode == "Kväll":
            self.select_option("input_select.house_modes", "Natt")
            self.debug_log()

    def dag(self, kwargs):
        current_mode = self.get_current_mode()
        if current_mode == "Morgon" or current_mode == "Natt":
            self.select_option("input_select.house_modes", "Dag")
            self.debug_log()

    def kvall(self, kwargs):
        current_mode = self.get_current_mode()
        if current_mode == "Dag":
            self.select_option("input_select.house_modes", "Kväll")
            self.debug_log()

    def get_current_mode(self):
        mode = self.get_state("input_select.house_modes")
        return mode

    def debug_log(self):
        mode = self.get_current_mode()
        self.call_service("logbook/log", name="{}".format(self.name), message=mode)
        self.call_service("notify/calle", title="HouseMode", message=mode)
