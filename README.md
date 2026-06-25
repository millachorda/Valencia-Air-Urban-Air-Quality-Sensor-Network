# Valencia Air - Urban Air Quality Sensor Network

This is a network made up of three DIY sensor nodes. This sensors monitors the air quality across three different environments of the city of Valencia, Spain. There will be one of this nodes in the city centre, another one in the urban periphery and the last one one the more beach part. There will also be a live web map comparing all of the three zones in real time.

---

## What does it do?

Each node measures particulate matter (PM1.0 / PM2.5 / PM10), temperature, humidity, pressure, CO2 levels and VOC levels. Readings are sent over WiFi every 60 seconds to a backend that stores the data and pushes live updates to an interactive map of Valencia. Each location shows up as a colored pin, with historical charts and a it changes color when PM2.5 is very high, normal or very low.

The goal is to see the differences on pollution all around the three environments making it visible and comparable.

## Why this locations?

| Node | Location | Environment |
| -----|----------|-------------|
| Node 1 | City center | Dense residential / urban |
| Node 2 | Periphery | Higher traffic and industry |
| Node 3 | Coastal natural park | Clean air by the sea |

The coastal node sits in a high marine humidity, so its particulate readings are humidity-corrected using the BME280 data.

## Hardware

Each node is built around an ESP32. Bill of materials per node:

| Component | Function | Interface |
|-----------|----------|-----------|
| ESP32 Devkit (USB-C) | Microcontroller + WiFi | - |
| PMS5003 | Particulate matter PM1.0 / PM2.5 / PM10 | UART (5V) |
| BME280 | Temperature, humidity, pressure | I2C |
| SGP30 | CO2-equivalent, VOC | I2C |
| 5V / 2A USB-C power supply | Power | - |
| 0.96" OLED display | local readings | I2C

Node 3 has an IP65 weatherproof enclosure with cable glands for the more humid environment.

## Wiring (per node)

Three I2C devices share the same two pins. The PMS5003 uses a separate UART. Everything shares a common ground.

| Connection | ESP32 pin |
|------------|-----------|
| I2C SDA (BME280, SGP30, OLED) | GPIO21 |
| I2C SCL (BME280, SGP30, OLED) | GPIO22 |
| PMS5003 TX -> ESP32 | GPIO16 (RX2) |
| PMS5003 RX -> ESP32 | GPIO17 (TX2) |
| I2C sensors VCC | 3V3 |
| PMS5003 VCC | 5V (VIN) |
| All GND | GND |

The PMS5003 outputs only 3.3V even when powered by a 5V power supply.

## Software

- Firmware: Arduino on the ESP32. Libraries that I will use: 'Adafruit_BME280', 'Adafruit_SGP30', 'PMS', 'Adafruit_SSD1306'.
- Backend: Python + Flask REST API, SQLite database. [Website of the map](https://valencia-air.milla-chorda.hackclub.app)
- Frontend: The map HTML.