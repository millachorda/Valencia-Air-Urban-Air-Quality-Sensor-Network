# Valencia Air - Urban Air Quality Sensor Network

This is a live project that consists on 3 DIY nodes on different places on the city of Valencia in Spain. One node in the beach, another of those nodes in a more dense area with more movement and a node on a street that there are cars always going through

---

## What does it do?

Each node measures the temperature, the CO2 in ppm, the Particulate Matter (PM1.0, PM2.5, PM10) in µg/m³, the humidity and the pressure in hPa.

The goal is to see the differences on this zones in real time.

## Why this locations?

| Node | Location | Environment |
| -----|----------|-------------|
| Node 1 | City center | Dense residential |
| Node 2 | Periphery | High traffic |
| Node 3 | Beach | Clean air by the sea |

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


## Software

- Firmware: Arduino on the ESP32. Libraries that I will use: 'Adafruit_BME280', 'Adafruit_SGP30', 'PMS', 'Adafruit_SSD1306'.
- Backend: Python + Flask REST API, SQLite database. [Website of the map](https://valencia-air.milla-chorda.hackclub.app)
- Frontend: The map HTML.