import appdaemon.plugins.hass.hassapi as hass

from typing import Callable

#
# Hello World App
#
# Args:
#

class HelloWorld(hass.Hass):

    def initialize(self):
        self.log("Hello from AppDaemon")
        self.log("You are now ready to run Apps!")

        # bool_exist = self.get_state("input_boolean.AD_{}".format(self.name))
        # if bool_exist is None:
        #     friendly_name = self.name.replace('_', ' ').title()
        #     self.log("AppName: {}".format(friendly_name))
        #     self.attributes = {}
        #     self.attributes['friendly_name'] = friendly_name
        #     # self.attributes['icon'] = "mdi:language-python"
        #     self.set_state("input_boolean.AD_{}".format(self.name),
        #                    state='on', 
        #                    attributes=self.attributes)
        #     self.call_service("logbook/log", name="{}".format(self.name), message='Init bool')
