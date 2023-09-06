```mermaid
C4Context
title Sensor-Hub
Boundary(b0, "sensor_hub") {
    System(network, "Networking")
    System(database, "DATABASE")
    System(broker, "MQTT Broker")
    System(client, "MQTT client")
    System(viz_server, "Visualization Server")
}
```