"""Example script bridging mqtt pubsub with udp"""

import threading
import queue
import socket
import json
import paho.mqtt.client as mqtt

CLIENT_ID = 1

MQTT_BROKER = "wiselambda4.andrew.cmu.edu"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_SUBSCRIBE_TOPIC = f"outgoing/{CLIENT_ID}"
MQTT_PUBLISH_TOPIC_PREFIX = "receive/"

UDP_IP = "0.0.0.0"
UDP_PORT = (10000 + CLIENT_ID)  # Workaround diff ports on same machine 
MTU_SIZE = 1472

mqtt_to_udp_queue = queue.Queue()
udp_to_mqtt_queue = queue.Queue()


# MQTT CLIENT STUFF, REPLACE W/ ROS2 CLIENT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        userdata["logger"]("Connected to MQTT Broker")
        client.subscribe(MQTT_SUBSCRIBE_TOPIC)
    else:
        userdata["logger"](f"MQTT Broker connect failed: {rc}")


def on_message(client, userdata, msg):
    """Callback when a message is received from MQTT."""
    try:
        mqtt_topic = msg.topic
        mqtt_payload = msg.payload.decode("utf-8")
        userdata["logger"](f"Received MQTT message on {mqtt_topic}: {mqtt_payload}")
        json_payload = json.loads(mqtt_payload)

        # Same as for ROS2, just add to queue for UDP thread
        udp_dest_ip = json_payload.get("ipv4_address", None)
        data = json_payload.get("data", None)
        if udp_dest_ip:
            mqtt_to_udp_queue.put((udp_dest_ip, data))
            userdata["logger"](
                f"Queued message to send via UDP to {udp_dest_ip}: {data}"
            )
    except Exception as e:
        userdata["logger"](f"Error in on_message: {e}")


def mqtt_thread(logger):
    client = mqtt.Client(userdata={"logger": logger})
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
    except Exception as e:
        logger(f"Unable to connect to MQTT Broker: {e}")
        return

    client.loop_start()

    while True:
        # Publish messages from the UDP queue to MQTT, replace with ROS2 publish
        if not udp_to_mqtt_queue.empty():
            try:
                mqtt_topic, mqtt_message = udp_to_mqtt_queue.get()
                client.publish(mqtt_topic, mqtt_message, qos=1)
                logger(f"Published to MQTT topic {mqtt_topic}: {mqtt_message}")
            except Exception as e:
                logger(f"Error publishing to MQTT: {e}")


# UDP SOCKET STUFF
def udp_thread(logger):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((UDP_IP, UDP_PORT))
    udp_sock.setblocking(False)
    logger(f"UDP socket listening on {UDP_IP}:{UDP_PORT}")

    while True:
        # Outgoing queue from MQTT to UDP
        if not mqtt_to_udp_queue.empty():
            try:
                udp_dest_ip, message = mqtt_to_udp_queue.get()
                dest_port = UDP_PORT + int(udp_dest_ip.split(".")[-1]) # Port offset workaround, remove later
                udp_sock.sendto(
                    message.encode("utf-8"), (udp_dest_ip, dest_port) 
                )
                logger(f"Sent UDP message to {udp_dest_ip}:{dest_port}: {message}")
            except Exception as e:
                logger(f"Error sending UDP message: {e}")

        # Incoming UDP to MQTT queue
        try:
            data, addr = udp_sock.recvfrom(MTU_SIZE)
            udp_source_ip = addr[0]
            udp_message = data.decode("utf-8")
            logger(f"Received UDP message from {udp_source_ip}: {udp_message}")

            # Determine MQTT topic based on UDP source IP, maybe use explicit source data field
            mqtt_topic = MQTT_PUBLISH_TOPIC_PREFIX + str(udp_source_ip.split(".")[-1])

            # Queue the message for publishing to MQTT
            udp_to_mqtt_queue.put((mqtt_topic, udp_message))
            logger(
                f"Queued message to publish to MQTT topic {mqtt_topic}: {udp_message}"
            )
        except BlockingIOError:
            pass


def logger(message):
    print(f"[{threading.current_thread().name}] {message}")


def main():
    # TODO: REPLACE MQTT client threads with some ROS2 client.
    mqtt_worker = threading.Thread(
        target=mqtt_thread, args=(logger,), name="MQTT-Thread", daemon=True
    )
    mqtt_worker.start()

    # UDP socket handler thread
    udp_worker = threading.Thread(
        target=udp_thread, args=(logger,), name="UDP-Thread", daemon=True
    )
    udp_worker.start()

    while True:
        threading.Event().wait(1)


if __name__ == "__main__":
    main()
