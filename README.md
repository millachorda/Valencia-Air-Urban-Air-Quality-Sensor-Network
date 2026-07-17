# Valencia Air — Urban Air Quality Sensor Network

A network of three DIY sensor nodes monitoring air quality across three
different environments in Valencia, Spain: the city center, the urban
periphery, and the coastal natural park of El Saler. A live web map compares
all three zones in real time.

**Live map:** https://valencia-air.milla-chorda.hackclub.app

---

## What does it do?

Each node measures particulate matter (PM1.0 / PM2.5 / PM10), temperature,
humidity, barometric pressure, CO2 and VOC levels. Readings are sent over WiFi
every 60 seconds to a Flask backend that stores them in SQLite and pushes live
updates to an interactive map of Valencia. Each location shows up as a colored
pin with historical charts, and the pin changes color depending on whether PM2.5
is low, normal or high.

The goal is to make the pollution differences between the three environments
visible and comparable.

## Why these locations?

| Node | Location | Environment |
|------|----------|-------------|
| Node 1 | City center | Dense residential / urban |
| Node 2 | Periphery | Higher traffic and industry |
| Node 3 | El Saler (coastal natural park) | Clean air by the sea |

The coastal node sits in high marine humidity, which inflates raw particulate
readings through hygroscopic growth — water condenses on particles and they
scatter more light. Node 3's PM readings are therefore humidity-corrected in
firmware using the BME280's relative humidity (`COASTAL_NODE` flag).

---

## Hardware

Each node is built around an ESP32. All three nodes are identical.

| Component | Function | Interface | I2C address |
|-----------|----------|-----------|-------------|
| ESP32 DevKit (USB-C) | Microcontroller + WiFi | — | — |
| PMS5003 | Particulate matter PM1.0 / PM2.5 / PM10 | UART @ 9600 | — |
| SCD41 | True CO2 (photoacoustic NDIR), temp, humidity | I2C | `0x62` |
| SGP30 | VOC / eCO2 | I2C | `0x58` |
| BME280 | Temperature, humidity, pressure | I2C | `0x76` |
| 0.96" OLED display | Local readings | I2C | `0x3C` |
| 5V / 2A USB-C power supply | Power | — | — |
| IP65 enclosure + cable glands | Weatherproofing | — | — |

Full bill of materials with prices, suppliers and component rationale:
**[Hardware/BOM.md](Hardware/BOM.csv)**

### Why SCD41 *and* SGP30

The SGP30 does not measure CO2 — it estimates it (eCO2) by correlating with VOC
readings. Outdoors, with no indoor VOC sources, that estimate sits at its
400 ppm floor and carries no information. Since this project exists to compare
CO2 across three environments, the measurement has to be real: the SCD41 does it
by photoacoustic NDIR, ±(50 ppm + 5%). The SGP30 stays because the SCD41 does
not measure VOCs, and the project publishes VOC levels. Together they cover both
properly.

### Why the BME280 is kept

The SCD41 also reports temperature and humidity, but the humidity correction on
Node 3 needs an independent RH source, and the BME280 additionally provides
barometric pressure. The two temperature readings cross-validate each other.

---

## Wiring

![Wiring diagram](Hardware/CAD/circuit_image.svg)

Four I2C devices share the same two pins; the PMS5003 uses a separate hardware
UART. Everything shares a common ground.

| Connection | ESP32 pin |
|------------|-----------|
| I2C SDA (SCD41, SGP30, BME280, OLED) | GPIO21 |
| I2C SCL (SCD41, SGP30, BME280, OLED) | GPIO22 |
| PMS5003 TX → ESP32 | GPIO16 (RX2) |
| PMS5003 RX → ESP32 | GPIO17 (TX2) |
| SGP30 / BME280 / OLED VCC | 3V3 |
| SCD41 VDD | 5V (VIN) |
| PMS5003 VCC | 5V (VIN) |
| All GND | GND |
| PMS5003 SET / RST | not connected |

**Note on the PMS5003 supply:** it needs a real 5 V rail — the laser and the fan
will not run on 3.3 V. Its **UART logic**, however, is 3.3 V, which is why its
TX line connects straight to the ESP32 with no level shifter.

**Note on the SCD41 supply:** it accepts 2.4–5.5 V, but it is powered from VIN
rather than 3V3 because it draws ~200 mA peaks during measurement, which would
load the ESP32's onboard regulator that already feeds the other three I2C
devices.

The four I2C addresses do not collide, so all four devices coexist on one bus.

---

## Mechanical design

The enclosure itself is a commercial CPROSP IP65 box (150×110×70 mm). The
custom parts are what goes inside and on it:

| Part | Purpose |
|------|---------|
| `mounting_plate` | Interior tray holding ESP32, SCD41, SGP30, BME280 and PMS5003 |
| `oled_bezel` | Frame holding the OLED behind a sealed polycarbonate window |
| `pms_duct` | Dual-port air duct with PTFE membrane pockets |

**[Hardware/CAD/valencia_air_node.step](Hardware/CAD/valencia_air_node.step)** — all three parts in one STEP file
**[Hardware/CAD/valencia_air_enclosure.py](Hardware/CAD/valencia_air_enclosure.py)** — parametric CadQuery source
STL files for printing are in the same folder.

Two design decisions worth calling out:

- **All sensors sit inside the enclosure, and the BME280 sits in the PMS5003's
  air intake path.** A temperature/humidity sensor floating loose inside a
  closed box measures the box, not the atmosphere — under direct sun that reads
  as much as 10 °C high, and since warming air drops relative humidity, the
  error would propagate straight into Node 3's humidity correction. Mounting the
  BME280 next to the duct intake means the PMS5003's own fan continuously pulls
  outside air across it. Some solar bias remains, so nodes are mounted in shade.
- **The OLED window is sealed; all airflow goes through the duct.** The PMS5003
  has separate air inlet and outlet, so it gets two dedicated downward-facing
  ports covered with PTFE membrane. Drilling those ports means the enclosure is
  no longer strictly IP65 — it is effectively ~IP54 (rain-protected). This is
  standard for outdoor air quality stations: a particulate sensor in a truly
  sealed box measures nothing.

Build steps: **[Hardware/ASSEMBLY.md](Hardware/ASSEMBLY.md)**

---

## Software

### Firmware — [`firmware/valencia_air_node.ino`](firmware/valencia_air_node.ino)

Arduino on the ESP32. Sensors are **autodetected** at boot via an I2C scan: any
sensor that is absent is reported as `null` and the node keeps running, so a
single dead module never takes a node offline. The PMS5003 frame is parsed
directly from `Serial2` (32-byte frames, `0x42 0x4D` header, checksum verified).

Libraries: `Sensirion I2C SCD4x`, `Adafruit_SGP30`, `Adafruit_BME280`,
`Adafruit_SSD1306`, `Adafruit_GFX`, `Adafruit_Unified_Sensor`.

Per-node configuration lives at the top of the file (`NODE_ID`, `NODE_NAME`,
`COASTAL_NODE`, WiFi credentials, `API_URL`).

### Backend — `backend/app.py`

Python + Flask REST API with a SQLite database.

| Route | Method | Purpose |
|-------|--------|---------|
| `/data` | POST | Nodes publish readings here |
| `/readings/<node>` | GET | Historical readings for one node |
| `/` | GET | Serves the map |

Expected JSON payload:

```json
{"node":3,"pm1":4,"pm25":7,"pm10":9,"temp":24.1,"humidity":68.2,"pressure":1014.1,"co2":421,"voc":18}
```

### Frontend — `frontend/`

HTML map with a colored pin per node and historical charts.

---

## Project status

| Milestone | Status |
|-----------|--------|
| ESP32 boots, connects to WiFi, publishes to backend | Done |
| BME280 reading and publishing live data | Done |
| Backend + live map deployed | Done |
| OLED display driver | Done |
| SCD41 / SGP30 integration | Pending hardware |
| PMS5003 integration | Pending hardware |
| Enclosure assembly and deployment | Pending |
