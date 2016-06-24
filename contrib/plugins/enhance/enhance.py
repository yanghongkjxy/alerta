
# This is an example Alerta server plugin used to enhance received alerts
# by adding, modifying or looking up alert attributes "on the fly".

# NOTE: This plugin should be modified to support your environment before use.

from alerta.plugins import PluginBase


class EnhanceAlert(PluginBase):

    def pre_receive(self, alert):
        alert.attributes['runBookUrl'] = 'http://www.mywiki.org/RunBook/%s' % alert.event.replace(' ', '-')
        return alert

    def post_receive(self, alert):
        return

    def status_change(self, alert, status, text):
        return
