# MRVizNet-The_Network_Visualizer_with_Mixed-Reality
MRVizNet is an immersive, low-latency spatial network monitoring framework designed to map real-time protocol-level traffic onto a 3D physical topology. By decoupling high-speed backend data collection from a rendering frontend, the system eliminates the cognitive friction of reading static 2D log tables (e.g., legacy Wireshark) and replaces them with an interactive 3D/Mixed Reality data plane.

The architecture is explicitly engineered for remote service validation, allowing an engineer to execute standalone telemetry analysis via an XR headset (such as Apple Vision Pro or Meta Quest) connected to remote infrastructure testbeds across different geographic regions. 
---

## 🛠 Architectural Overview & Data Flow

The platform utilizes an event-driven, decoupled publish-subscribe pipeline to achieve real-time synchronization between live network hardware and the visual presentation environment.

[ BACKEND: Live Wire Infrastructure ]
│
▼ (Kernel-level / Live Sniffing via Scapy)
[ wifi_packet_capture.py ]
│
▼ (Serialized JSON Payloads over TCP)
[ Mosquitto MQTT Broker ]  <─── (Local Server / Lab Host Gateway)
│
============ NETWORK / TIME-ZONE BOUNDARY ============
│
▼ (Subscribed via MQTTnet Client over Wi-Fi / 5G)
[ FRONTEND: Standalone MR Headset / Runtime Engine ]
│

├─── C# Data Ingestion Engine (MQTTReceiver.cs)
├─── Main-Thread Dispatcher Buffer (UnityMainThreadDispatcher.cs)
▼
[ 3D Spatial Topology ] (Dynamic Spawning & Raycast Inspection via PacketVisualizer.cs)

