import paho.mqtt.client as paho
import ssl
import logging
import json


logging.basicConfig(level=logging.INFO)


class MQTT:
    def __init__(self, queue, listener=False, topic="default"):
        self.queue = queue
        self.connected = False
        self.listener = listener
        self.topic = topic
        self.logger = logging.getLogger()


    def __on_connect(self, client, userdata, flags, rc):
        self.connected = True
        self.logger.info("Connected")
        if self.listener:
            self.mqttc.subscribe(self.topic)

        self.logger.debug(f'{rc}')

    def __on_message(self, client, userdata, message):
        payload = json.loads(message.payload.decode('utf-8'))
        self.queue.put(payload)
        self.logger.info(f'Topic: {message.topic}\nDevice Name: {payload["device_name"]}\nDevice Data: {payload["device_data"]}')


    def __on_log(self, client, userdata, level, buf):
        self.logger.debug(f'{userdata}, {level}, {buf}')

    def bootstrap_mqtt(self):
        self.mqttc = paho.Client()
        self.mqttc.on_connect = self.__on_connect
        self.mqttc.on_message = self.__on_message
        self.mqttc.on_log = self.__on_log

        aws_host = 'a399x4joyc6hal-ats.iot.eu-north-1.amazonaws.com'
        aws_port = 8883

        ca_path = './AmazonRootCA1.pem'
        cert_path = './953078c62d-certificate.pem.crt'
        key_path = './953078c62d-private.pem.key'

        self.mqttc.tls_set(ca_path,
                           cert_path,
                           key_path,
                           cert_reqs=ssl.CERT_REQUIRED,
                           tls_version=ssl.PROTOCOL_TLSv1_2,
                           ciphers=None)
        self.mqttc.connect(aws_host, aws_port, keepalive=120)

        return self

    def start(self):
        self.mqttc.loop_start()
        while True:
            if not self.connected:
                self.logger.debug("Attempting to connect.")


if __name__ == '__main__':
    MQTT(listener=True, topic='device/+/data').bootstrap_mqtt().start()

