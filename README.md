# MRVizNet: A Mixed Reality based Network Visualizer

MRVizNet is a project developed in Unity designed to visualize live network traffic in a 3D environment rather than relying entirely on static, text-based 2D logs like Wireshark. The intent is to bridge the gap between raw data extraction and spatial network monitoring.
It captures packets on a local network, parses their headers, and uses a 3D gaming engine to display packet streams moving dynamically between a source device and target wireless access points.

The project uses a Python-based packet sniffer as the backend, a local MQTT broker as the data pipeline, and a Unity-built frontend scene acting as the visual control plane.

---

## Architectural Overview & Data Flow

The project passes packet metadata from the live wire to the 3D scene using a lightweight publish-subscribe model over MQTT.

To visualize the Pub/Sub architecture better, think of it as a **Digital Post Office** system:
* **The Mail Sender (`wifi_packet_capture.py` / `mqttsender.py`):** The Python backend. It captures or simulates packet frames, writes down their metadata, and drops them off at the central post office.
* **The Post Office / Middleman (Mosquitto Broker):** The local MQTT Broker. It sits in the middle, keeping the specific channel (`network/packets`) open and routing incoming data safely.
* **The Recipient (Unity Engine):** The C# frontend. It continuously watches the channel, pulls down the packet data, and instantly draws it as a moving 3D object.

```
[ BACKEND: Local Wi-Fi Traffic ]
                │ 
                ▼ (Packet Sniffing via Scapy)
     [ Wifi Packet Captures ]
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
* **Serialization:** Extracts essential fields: Source IP, Destination IP, Protocol Type, and Packet Size—and packages them into plain JSON strings.

### 2. Messaging Pipeline (MQTT)
* **Broker:** Uses a local **Mosquitto MQTT Broker** to handle communication between Python and Unity.
* **Transport:** Since MQTT runs over TCP, it guarantees that packet metadata is delivered reliably and in the correct order.
* **Data Flow:** The Python script publishes to the `network/live_traffic` topic, acting as an event-driven stream.

### 3. Visual Layer (Unity 6 / C#)
* **Receiving:** `MQTTReceiver.cs` listens to the broker topic and parses incoming JSON strings.
* **Thread Management:** Because MQTT messages arrive on background threads, `UnityMainThreadDispatcher.cs` safely queues the incoming data so it can be handled by Unity's main rendering loop.
* **Rendering:** `PacketVisualizer.cs` instantiates 3D prefabs at the laptop source position and animates them along a `LineRenderer` path toward cylinders representing the Access Points (AP1, AP2, AP3).
* **Visual Coding:** Packets are color-coded by protocol (**Red** = TCP, **Blue** = UDP, **Green** = HTTP, **Yellow** = FTP) and visually scaled based on their actual packet size.

## Project Requirements

### Software & Libraries
* **Python Backend:** `paho-mqtt`, `scapy` (install via `pip install paho-mqtt scapy`)
* **MQTT Broker:** Eclipse Mosquitto (running locally on default port 1883)
* **Unity 6 Packages:** * `M2Mqtt` (MQTT client for Unity)
  * `Newtonsoft.Json` (JSON parsing)
  * `TextMeshPro` (UI rendering)

### Environment Assets
* **Source Node:** 3D model representing the local host laptop.
* **Destination Nodes:** Three distinct 3D cylinders representing target Wireless Access Points (`AP1`, `AP2`, `AP3`).
* **Packet Prefab:** A basic geometric primitive equipped with a `BoxCollider` (for selection tracking) and a `LineRenderer` (to trace the motion vector).

---

## Step-by-Step Implementation & Workflow

### 1. Hardware & Environment Setup
1. Deploy the local **Mosquitto MQTT Broker** on the host engine.
2. Structure the Unity scene layout by establishing the base coordinates for the Laptop transform and positioning the three target Access Point cylinders.
3. Attach the `MQTTReceiver.cs` script to an empty `NetworkManager` GameObject to handle initialization sockets.

### 2. Execution & Execution Testing
1. Spin up the packet ingestion pipeline by running the target python script from the terminal:`python wifi_packet_capture.py`
(Note: mqttsender.py can alternatively be executed to stream predictable mock data profiles for offline logic validation).
2. Initialize the Unity runtime environment.
3. Observe the `PacketVisualizer.cs` spawning instances of the packet prefab at the Laptop coordinate path, updating materials based on the incoming JSON protocol flags, and moving them linearly toward the designated target AP.
4. Interact with any flying packet asset by hovering or left-clicking; the `Raycasting.cs` engine catches the collider collision and forces `UIManager.cs` to print the underlying text data arrays to the on-screen Canvas panel.

---

## Repository Project Hierarchy
```
MRVizNet-Project/
│
├── Backend/
│   ├── mr_wifi_packet_capture.py     # Live Scapy packet sniffer & publisher
│   └── mr_mqttsender.py              # Mock telemetry simulation data script
│
└── Frontend/
    ├── Scenes/
    │   └── MainSceneMR.unity        # Main topology environment setup
    │
    ├── Scripts/
    │   ├── MQTTReceiver.cs        # Threaded broker connection listener
    │   ├── UnityMainThreadDispatcher.cs # Thread-safe queue manager
    │   ├── PacketVisualizer.cs    # Spawning, scaling, and path animation
    │   ├── PacketInfo.cs          # Local packet telemetry storage class
    │   ├── Raycasting.cs          # Raycast collision object selector
    │   └── UIManager.cs           # Canvas TextMeshPro layout controller
    │
    └── Materials/
        ├── TCP_Red.mat
        ├── UDP_Blue.mat
        ├── HTTP_Green.mat
        └── FTP_Yellow.mat
```

---

## Future Development Scope

* **Headset Porting:** Porting the runtime layout over to standalone VR headsets (e.g., Meta Quest 3 or Apple Vision Pro) via the Unity XR Interaction Toolkit to view the topology within a true spatial context.
* **Advanced Telemetry Metrics:** Extending the Python parsing dictionary to calculate throughput rates and link drop counts per Access Point destination.
* **Expanded Protocol Support:** Adding packet identification filters for structural core protocols like ICMP, DNS, and ARP.
