import appdaemon.plugins.hass.hassapi as hass
import datetime


class LightScheduleMorning(hass.Hass):
    """

    morning_light_week:
      module: light_schedule_morning
      class: LightScheduleMorning
      motion_sensor: binary_sensor.motion_sensor_158d0001f9d45b
      activate_time: "06:00:00"
      deactivate_time: "07:35:00"
      lights:
        - light: light.entity
        brightness: 147
        - light: light.entity

    Arguments:

    """

    def initialize(self):
        self.log("LightScheduleMorning init")
        try:
            self.motion_sensor = self.args["motion_sensor"]
            self.activate_time = self.args["activate_time"]
            self.deactivate_time = self.args["deactivate_time"]
        except KeyError as e:
            self.log("Argument not found : {}".format(e), level="ERROR")
            return

        time_off = self.parse_time(self.deactivate_time)
        time_off = (datetime.datetime.combine(datetime.date(1, 1, 1),
                    time_off) + datetime.timedelta(minutes=1)).time()

        if "lights" in self.args:
            for light in self.args["lights"]:

                if "brightness" in light:
                    brightness = light["brightness"]
                else:
                    brightness = 0

                light = light["light"]
                self.run_daily(self.light_off, time_off, light=light)
                self.listen_state(self.motion,
                                  self.motion_sensor,
                                  new="on",
                                  constrain_start_time=self.activate_time,
                                  constrain_end_time=self.deactivate_time,
                                  light=light,
                                  brightness=brightness)

                self.log("light:{}, motion_sensor:{}, activate_time:{}, deactivate_time:{}, brightness:{}, time_off:{}\n"
                         .format(self.friendly_name(light),
                                 self.friendly_name(self.motion_sensor),
                                 self.activate_time,
                                 self.deactivate_time,
                                 brightness,
                                 time_off))
        else:
            self.log("Argument not found: lights", level="ERROR")
            return

    def motion(self, entity, attribute, old, new, kwargs):
        self.log("Line: __line__, Function: __function__")
        self.state = self.get_state(kwargs["light"])

        if self.state == "off":
            if kwargs["brightness"]:
                self.turn_on(kwargs["light"], brightness=kwargs["brightness"])
            else:
                self.turn_on(kwargs["light"])

            self.log("Line: __line__, Function: __function__, Message: Turn on {} with brightness {}\n"
                     .format(self.friendly_name(kwargs["light"]), kwargs["brightness"]))

    def light_off(self, kwargs):
        self.log("Line: __line__, Function: __function__")
        self.turn_off(kwargs["light"])
        self.log("Line: __line__, Function: __function__, Message: Turn off {}\n"
                 .format(self.friendly_name(kwargs["light"])))
