# This file Replaces the file homeassistant/components/mqtt/discovery.py
#
# Example of a homie properties, node and device layout that this very hacked together version works for.
# [homeassistant.components.mqtt.discovery] Online Match[templux1]: true
# [homeassistant.components.mqtt.discovery] Device:[templux1] - Node:[temperature] - Prop:[unit] - Value:[c]
# [homeassistant.components.mqtt.discovery] Device:[templux1] - Node:[temperature] - Prop:[temperature] - Value:[27.84]
# [homeassistant.components.mqtt.discovery] Found new component: sensor templux1_temperature
#
# devices/templux1/$online true
# devices/templux1/temperature/$properties unit,temperature
# devices/templux1/temperature/unit c
# devices/templux1/temperature/temperature 27.84


import asyncio
import json
import logging
import re
import paho.mqtt.client as mqtt
import json
import time
import threading

class HomieAdapter:
    """ Class for controlling Homie Convention.
        The Homie Convention follows the following format:
        root/system name/device class (optional)/zone (optional)/device name/capability/command  """

    _LOGGER = logging.getLogger(__name__)

    messages = {}
    nodes = {}

    TOPIC_NODES = re.compile(r'(?P<prefix_topic>[$\w]+[-\w]*\w)/(?P<device>[$\w]+[-\w]*\w)/\$nodes')
    TOPIC_ONLINE = re.compile(r'(?P<prefix_topic>[$\w]+[-\w]*\w)/(?P<device>[$\w]+[-\w]*\w)/\$state')
    TOPIC_NODE_PROPERTIES = re.compile(
        r'(?P<prefix_topic>[$\w]+[-\w]*\w)/(?P<device>[$\w]+[-\w]*\w)/(?P<node>[$\w]+[-\w]*\w)/\$properties')

    STATE_ONLINE = 'ready'
    ALREADY_DISCOVERED = 'mqtt_discovered_components'


    def __init__(self, host, port, root, authentication, login, password):
        try:
            self.mqttc = mqtt.Client()
            self.mqttc.on_message = self.on_message
            print("Homey discovery started.....")
            self.mqttc.connect(host, int(port), 60)
            self.mqttc.subscribe("homie/homey-5d667df592e8eb0c7d3f1022/#", 2)
            threading.Thread(target=self.startloop).start()
        except KeyboardInterrupt:
            print("Received topics:")
            #print(self.getdevices())


    def startloop(self):
        self.mqttc.loop_forever()

    def on_message(self,mqttc, obj, msg,):
        qos = 0
        """Process the received message."""


        # List of all topics published on MQTT since HA was started
        payload = msg.payload.decode("utf-8")
        topic = msg.topic
        #self._LOGGER.warning("mqdiscover | [%s]:[%s]:[%s]", qos, topic, payload)
        self.messages[topic] = payload
        #print(topic+"====>"+self.messages[topic])

        # Check if the topic is a list of nodes
        match_nodes = self.TOPIC_NODES.match(topic)
        if match_nodes:
            #print(payload)
            arr = payload.split(",")
            nodelist = {}
            for a in arr:
            #    b = a.split(':')
            #    nodelist[b[0]] = b[1]
                nodelist[a] = ""
            device = match_nodes.group('device')
            self.nodes[device] = nodelist
            # for key, val in nodes.items():
            # for key2, val2 in val.items():
            # _LOGGER.warning("Device:[%s] - Node:[%s] - Type:[%s]", key, key2, val2)
            print(self.nodes)
        # Check if topic is $online topic
        # Check if topic is $online topic
        match_online = self.TOPIC_ONLINE.match(topic)
        if match_online:
            self._LOGGER.warning("Online Match[%s]: %s", match_online.group('device'), payload)
            if payload.lower() == self.STATE_ONLINE:
                device = match_online.group('device')
                base_topic = match_online.group('prefix_topic')


                for m_key in list(self.messages):
                    #print(m_key)
                    match_node_prop = self.TOPIC_NODE_PROPERTIES.match(m_key)
                    #print(match_node_prop)
                    #print(device)
                    if match_node_prop:
                        if match_node_prop.group('device') == device:
                            node = match_node_prop.group('node')
                            config = {}
                            for prop in self.messages[m_key].split(','):
                                self._LOGGER.warning("Device:[%s] - Node:[%s] - Prop:[%s] - Value:[%s]", device, node, prop,
                                                self.messages['{}/{}/{}/{}'.format(base_topic, device, node, prop)])

                               # if prop == 'unit':
                                   # unit = self.messages[
                                   #     '{}/{}/{}/{}'.format(base_topic, device, node, prop)]
                                #else:
                                    #print("check")
                                    #statetopic = '{}/{}/{}/{}'.format(base_topic, device, node, prop)
                                    #devicename = self.messages['{}/{}/$name'.format(base_topic, device)] + ' ' + prop
                                    #print("check2")
                            platform = 'mqtt'
                            component = 'sensor'
                            #config[self.CONF_PLATFORM] = platform
                           # if ALREADY_DISCOVERED not in hass.data:
                           #     hass.data[ALREADY_DISCOVERED] = set()

                            discovery_id = '_'.join((device, node))
                            #discovery_hash = (component, discovery_id)

                           # if discovery_hash in hass.data[ALREADY_DISCOVERED]:
                           #     _LOGGER.info("Component has already been discovered: %s %s",
                           #                  component, discovery_id)
                           #     return

                           # hass.data[ALREADY_DISCOVERED].add(discovery_hash)

                            self._LOGGER.info("Found new component: %s %s", component, discovery_id)
                            print(("Found new component: %s %s", component, discovery_id))


        #return null

