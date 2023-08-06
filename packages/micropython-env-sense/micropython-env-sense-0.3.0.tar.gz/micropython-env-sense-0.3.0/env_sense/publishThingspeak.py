# https://opensource.org/licenses/GPL-3.0
# Publish to a thingspeak channel via MQTT

from umqtt.robust import MQTTClient


class ThingspeakMqtt:
    def __init__(self, channel_id=None, write_api_key=None):
        myMqttClient = b'client_981f1b00'  # TODO: put in config

        THINGSPEAK_URL = b"mqtt.thingspeak.com"
        self.client = MQTTClient(client_id=myMqttClient,
                                 server=THINGSPEAK_URL,
                                 ssl=False)
        self.client.connect()
        self.set_channel_info(channel_id, write_api_key)

    def set_channel_info(self, channel_id, write_api_key):
        self.channel_id = channel_id
        self.write_api_key = write_api_key

    def publish(self, payload):
        credentials = bytes("channels/{:s}/publish/{:s}".format(
            self.channel_id, self.write_api_key), 'utf-8')
        mqtt_payload = ['{key}={val}'.format(key=key, val=val) for key, val in payload.items()]
        mqtt_payload = '&'.join(mqtt_payload) + '\n'
        mqtt_payload = bytes(mqtt_payload, 'utf-8')
        self.client.publish(credentials, mqtt_payload)
