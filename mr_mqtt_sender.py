"""
MRVizNet-3D_Network_Visualizer

Author: Sneha Sugilal

Think of the MQTT Broker as a digital post office.
In our digital post office analogy, if the MQTT Broker is the central sorting office,
mqttsender.py is the Mail Sender dropping off stamped letters.

The Architecture Analogy:
1. THE SENDER (This File): Acts as the Mail Sender. It writes telemetry logs
   and drops them off at the central post office under a specific P.O. Box channel.
2. THE BROKER (Mosquitto): The Central Post Office/Middleman. It holds the P.O. Box
   ("network/packets") open and routes the mail.
3. THE SUBSCRIBER (Unity): The Recipient standing by the mailbox waiting to read
   the letters and draw them in 3D.
"""


import json
import random
import time
import paho.mqtt.client as mqtt

# Network Setup with MQTT Broker
BROKER = "localhost"                # Replace with the actual IP of the laptop running Mosquitto
TOPIC = "network/packets"           # A specific mailbox
SOURCE_LAPTOP_IP = "10.110.76.7"    # Source Laptop IP Address

# Defining 3 Access points as a Dict with their IP addresses
access_points = {
    "AP1": "10.110.0.10",
    "AP2": "10.110.0.11",
    "AP3": "10.110.0.12"
}

# Initialize MQTT Client and Connection
client = mqtt.Client()
client.connect(BROKER, 1883, 60)  # 1883 is the standard network port for MQTT, 60 is the "keepalive" timer in seconds
client.loop_start()               # Keeps the connection stable in the background


def send_packet():
    packet_types = ["TCP", "UDP", "HTTP", "FTP"]

    while True:
        packet_type = random.choice(packet_types)
        ap_name = random.choice(list(access_points.keys()))
        ap_ip = access_points[ap_name]
        message = f"Data sent from {SOURCE_LAPTOP_IP} to {ap_name} ({ap_ip})"
        packet_size = len(message.encode('utf-8')) + random.randint(100, 1000)  # Packet size in bytes
        # No hard network rule here; it is purely for realistic simulation.
        # In real life, network packets fluctuate in size.
        packet = {                     # variable as a dictionary mirroring an IP packet header
            "type": packet_type,
            "size": packet_size,
            "message": message,
            "destination": ap_name,
            "destination_ip": ap_ip,
            "source_ip": SOURCE_LAPTOP_IP,
            "timestamp": time.time()
        }

        # Publish the packet to the MQTT broker
        client.publish(TOPIC, json.dumps(packet))
        # "Dumps" the Python dictionary object
        #  Converts it into a universally readable plain-text string aka the JSON format
        # .publish(...) physically shoots it across the network into designated TOPIC channel
        print(f"Sent: {packet}")

        time.sleep(30)  # Sends a packet every 30 seconds


if __name__ == "__main__":
    send_packet()
