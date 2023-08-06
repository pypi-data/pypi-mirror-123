"""MQTT"""
import json
import paho.mqtt.client as mqtt

LOCAL_ADDRESS = "thingbits.local"
LOCAL_TOPIC = "thingbits/sensors"

device_list = []

def listen(device_id, user_data, callback):
    """
    Listen for MQTT events from device_id.  When event happens,
    calls callback(device_id, user_data, sensor_data)
    """
    userdata = {
        "device_id": device_id,
        "user_data": user_data,
        "callback": callback
    }

    client = mqtt.Client(userdata = userdata)
    client.on_connect = on_listen_connect
    client.on_message = on_listen_message
    try:
        client.connect(LOCAL_ADDRESS)
        client.loop_start()
    except:
        pass

def on_listen_connect(client, userdata, flags, rc):
    client.subscribe(LOCAL_TOPIC + "/" + userdata["device_id"], 0)

def on_listen_message(client, userdata, msg):
    global device_list
    
    payload_text = msg.payload.decode("utf-8").strip('\x00')
    payload_obj = json.loads(payload_text)
    userdata["callback"](userdata["device_id"], userdata["user_data"], payload_obj["data"])

def devices():
    """ Discovery of Devices Connected To ThingBits Hub """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(LOCAL_ADDRESS)
        for i in range(256):
            client.loop(timeout=(1.0 / 256.0))
        return device_list
    except:
        return []


def discover():
    """ Discovery of ThingBits Hub """
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect(LOCAL_ADDRESS)
        client.disconnect()
        return [()]
    except:
        return []

def on_connect(client, userdata, flags, rc):
    client.subscribe(LOCAL_TOPIC, 0)

def on_message(client, userdata, msg):
    global device_list
    
    payload_text = msg.payload.decode("utf-8").strip('\x00')
    payload_obj = json.loads(payload_text)
    device_list = payload_obj['sensors']
    client.disconnect()
