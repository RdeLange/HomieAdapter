import paho.mqtt.client as mqtt
import json
import time
import threading

class HomieAdapter:
    """ Class for controlling Homie Convention.
        The Homie Convention follows the following format:
        root/system name/device class (optional)/zone (optional)/device name/capability/command  """

    DEVICES = []

    def __init__(self,host, port,root,authentication,login,password):
        try:
            self.mqttc = mqtt.Client()
            self.mqttc.on_message = self.on_message
            print("Homey discovery started.....")
            self.mqttc.connect(host, int(port), 60)
            self.mqttc.subscribe("homie/homey-5d667df592e8eb0c7d3f1022/#", 1)
            threading.Thread(target=self.startloop).start()
        except KeyboardInterrupt:
            print("Received topics:")
            print(self.getdevices())


    def startloop(self):
        self.mqttc.loop_forever()


    def on_message(self,mqttc, obj, msg,):
        #INITIAL VALUES
        payload = str(msg.payload)
        topic = str(msg.topic)

        #Update DEVICES DB
        #print(topic)
        self.updatedevice(topic,payload)



    def updatedevice(self,topic,payload):

        cells = topic.split("/")
        #print(cells)
        devicetopic = cells[0] + "/" + cells[1] + "/" + cells[2] + "/"
        #if devicetopic not in self.DEVICES:
        #    self.DEVICES[devicetopic] = {}
        #print(len(cells))
        if len(cells) >3:
            result = cells[3].find("$")


            if result > -1:
                result2 = cells[3].find("$properties")
                if result2 >-1:
                    specificproperties = payload.split(",")
                    i = 0
                    print(len(specificproperties))
                    while i < len(specificproperties):
                        print(specificproperties[i])
                        self.DEVICES[cells[0] + "/" + cells[1] + "/" + cells[2] + "/"][specificproperties[i]] = ""
                        i += 1
                else:
                    property = cells[3][1:]  # $ from begining of property
                    self.DEVICES[cells[0] + "/" + cells[1] + "/" + cells[2] + "/"][property] = payload.decode("utf-8")


    def getdevices(self):
        results = []
        count =1
        print(self.DEVICES)
        for device in self.DEVICES:
            results.append({ "idx":count, "Name": device[1], "Type": device[2] , "Status":device[3][0], "Level":device[3][1],"Data":device[3][0] })
            count=count+1

                #print(results)
        result=json.dumps({'result': results})
        #print(self.DEVICES)
        return result
