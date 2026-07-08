# MRVizNet: The Immersive Visualizing Network with Mixed Reality

MRVizNet is a project built to visualize live network traffic in a 3D environment rather than relying entirely on static, text-based 2D logs like Wireshark. 
It captures packets on a local network, parses their headers, and uses a 3D gaming engine to display packet streams moving dynamically between a source device and target wireless access points.

The system is split into two parts: a Python backend that handles packet sniffing and data routing, and a Unity frontend that renders the 3D topology and handles user interactions.

---

## 🛠 Architectural Overview & Data Flow

The project passes packet metadata from the live wire to the 3D scene using a lightweight publish-subscribe model over MQTT.

```
[ BACKEND: Local Wi-Fi Traffic ]
                │ 
                ▼ (Packet Sniffing via Scapy)
     [ wifi_packet_capture.py ]
                │
                ▼ (JSON Payloads over TCP)
     [ Mosquitto MQTT Broker ]  (Running Locally)
                │
                ▼ (Subscribed via MQTT Client)
[ FRONTEND: Unity 6 Application ]
                │  
                ├─── Data Ingestion (MQTTReceiver.cs)
                ├─── Concurrency Queue (UnityMainThreadDispatcher.cs)
                ▼ 
       [ 3D Spatial Topology ] (Spawning & Interaction via PacketVisualizer.cs)
```
### 1. Data Capture Engine (Python)
* **Sniffing:** Uses `Scapy` to tap into the local wireless interface and capture live packet headers.
* **Filtering:** Filters out background traffic to isolate specific target protocols (TCP, UDP, HTTP, and FTP) so the frontend isn't flooded with junk data.
* **Serialization:** Extracts essential fields—Source IP, Destination IP, Protocol Type, and Packet Size—and packages them into plain JSON strings.

### 2. Messaging Pipeline (MQTT)
* **Broker:** Uses a local **Mosquitto MQTT Broker** to handle communication between Python and Unity.
* **Transport:** Since MQTT runs over TCP, it guarantees that packet metadata is delivered reliably and in the correct order.
* **Data Flow:** The Python script publishes to the `network/live_traffic` topic, acting as an event-driven stream.

### 3. Visual Layer (Unity 6 / C#)
* **Receiving:** `MQTTReceiver.cs` listens to the broker topic and parses incoming JSON strings.
* **Thread Management:** Because MQTT messages arrive on background threads, `UnityMainThreadDispatcher.cs` safely queues the incoming data so it can be handled by Unity's main rendering loop.
* **Rendering:** `PacketVisualizer.cs` instantiates 3D prefabs at the laptop source position and animates them along a `LineRenderer` path toward cylinders representing the Access Points (AP1, AP2, AP3).
* **Visual Coding:** Packets are color-coded by protocol (**Red** = TCP, **Blue** = UDP, **Green** = HTTP, **Yellow** = FTP) and visually scaled based on their actual packet size.
