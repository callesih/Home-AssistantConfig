import appdaemon.plugins.hass.hassapi as hass

class XiaomiSwitch(hass.Hass):

  def initialize(self):
    self.log("Start xiaomi_switch")
    self.listen_event(self.one_click, event = None, entity_id = self.args["switch"]):

  def one_click(self, event_name, data, kwargs):
    self.log("Ett klick, event={}, data={}".format(event_name, data))

  def one_click(self, event_name, data, kwargs):
    self.log("Två klick")

  def one_click(self, event_name, data, kwargs):
    self.log("Lång klick")
