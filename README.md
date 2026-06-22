# Valencia Air - Urban Air Quality Sensor Network

This is a network consisting of three DIY sensor nodes that are monitoring the air quality across three different environments of the city of Valencia, Spain. There will be one DIY in the city centre, another one in the urban periphery and the last one one the more costal part. There will also be a live web map comparing all of the three zones in real time

---

## What does it do?

Each node measures particulate matter (PM1.0 / PM2.5 / PM10), temperature, humidity, pressure and the equivalent of CO2 / VOC levels. Readings are sent over WiFi every 60 seconds to a backend that stores the data and pushes live updates to an interactive map of Valencia. Each location shows up as a colored pin, with historical charts and a side-by-side comparison panel, plus a visual alert when PM2.5 exceeds the limit of 15 µg/m³.

The goal is to make pollution differences between this three environments visible and comparable - especially relevant in Valencia after the 2024 DANA floods.

## Why this locations?

| Node | Location | Environment | Expected results |
| -----|----------|-------------|------------------|
| Node 1 | City center | Dense residential / urban | Baseline urban readings |
| Node 2 | Periphery | Higher traffic and industry | Higher PM2.5 |
| Node 3 | Coastal natural park | Clean air by the sea | Lowest PM2.5, higher humidity |

The coastal node sits in ahigh marine humidity, so its particulate readings are humidity-corrected using the BM E280 data.

## Hardware

Each node is build around an ESP32. Bill of materials per node

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

The PMS5003 data line outputs 3.3V even when powered at 5V, so it connects directly to the ESP32 with no level shifter needed.

## Software

- Firmware: Arduino / C++ on the ESP32. Libraries: 'Adafruit_BME280', 'Adafruit_SGP30', 'PMS', 'Adafruit_SSD1306'.
- Backend: Python + Flask REST API, SQLite database, WebSockets for live updates. Hosted on [Nest](https://hacklub.app).
- Frontend: Leaflet.js map + Chart.js graphs, plain HTML/CSS/JS.

## Project status

- [] Node 1 - sensors reading and displaying locally
- [] Backend deployed and storing data
- [] Nodes 2 and 3 built and installed
- [] Live web map with all three nodes

## How to reproduce

1. Wire one node following the table above.
2. Flash the firmware in '/firmware' with WiFi credentials and backend URL.
3. Deploy the backend in '/backend' (instructions in that folder's README).
4. Open the frontend in '/frontend' - it connects to the backend and renders the map.

## About

A personal project by a 16-year-old maker in Valencia. built for Hack Club Macondo. The aim is a system that actually runs 24/7 in three real locations and can scale into a wider citizen sensor network.