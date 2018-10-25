import appdaemon.plugins.hass.hassapi as hass

class HouseModes(hass.Hass):

    def initialize(self):
        self.log("HouseModes init")

        self.listen_state(self.motion, self.args["motion_sensor"], new = "on")
        
        #self.run_daily(self.day, self.parse_time(self.args["day"]))
        #self.run_daily(self.evening, self.parse_time(self.args["evening"]))
        
        self.run_at_sunrise(self.day, offset=0)
        self.run_at_sunset(self.evening, offset=0)
        
    def motion(self, entity, attribute, old, new, kwargs):
        self.log("HouseModes motion")
        if self.now_is_between(self.args["morning"], "sunrise"):
            self.morning()

    def morning(self):
        self.log("HouseModes morning")
        morning_state = self.get_state("input_boolean.morning")
        self.log("HouseModes morning state={}".format(morning_state))
        if morning_state == "off":
            self.update_boolean("morning")
            self.log("HouseModes morning turn on morning")
        
            #self.turn_on("input_boolean.morning")
            #self.turn_off("input_boolean.day")
            #self.turn_off("input_boolean.evening")        
        #input_boolean.morning

    def day(self, kwargs):
        self.log("HouseModes day")
        self.turn_on("input_boolean.day")
        self.call_service("notify/telegram", title = "info", message = "HouseMode = Day")
        self.turn_off("input_boolean.morning")
        self.turn_off("input_boolean.evening")
        #input_boolean.day

    def evening(self, kwargs):
        self.log("HouseModes evening")
        self.turn_on("input_boolean.morning")
        self.call_service("notify/telegram", title = "info", message = "HouseMode = Evening")
        
        self.turn_off("input_boolean.morning")
        self.turn_off("input_boolean.day")
        #input_boolean.evening
        
    def night(self, kwargs):
        self.log("HouseModes night")
        
    def update_boolean(self, house_mode_bool):
        self.log("update event")
        house_modes = ["morning", "day", "evening", "night"]
        
        for modes in house_modes:
            #state = self.get_state("input_boolean.{}".format(modes))
            if house_mode_bool == modes:
                self.turn_on("input_boolean.{}".format(modes))
            else:
                self.turn_off("input_boolean.{}".format(modes))
        
        self.call_service("notify/telegram", title = "info", message = "HouseMode = {}".format(house_mode_bool))