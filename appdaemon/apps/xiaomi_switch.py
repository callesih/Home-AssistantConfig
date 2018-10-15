import appdaemon.plugins.hass.hassapi as hass

class XiaomiSwitch(hass.Hass):

    def initialize(self):
        self.listen_event(self.click, event = "click", entity_id = self.args["switch"])
    
    def click(self, event_name, data, kwargs):
        self.log("Ett klick registerat")
        click_type = data["click_type"]
    
        if click_type == "single":
            self.single()
        elif click_type == "double":
            self.double()
        elif click_type == "long_click_press":
            self.long_click()
        elif click_type == "hold":
            self.release_press()
        else:
            self.log("unknown click type={}".format(click_type))
    
    def single(self):
        self.log("single click")
    
    def double(self):
        self.log("double click")
    
    def long_click(self):
        self.log("long click")
    
    def release_press(self):
        self.log("release press")
