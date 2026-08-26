# Valencia Air — Urban Air Quality Sensor Network

Three DIY sensor nodes spread around Valencia, each one measuring the air in a
very different part of the city, all reporting to the same map.

**Live map:** https://valencia-air.milla-chorda.hackclub.app

> **TODO (write this part yourself):** why you started this. What made you want
> to measure the air here instead of just reading the official station data?
> Two or three sentences in your own words — this is the part a reader actually
> remembers, and nobody can write it for you.

---

## Status

Honest state of the project right now:

| Part | State |
|------|-------|
| Backend (Flask + SQLite) | Works. Running on Nest. |
| Frontend (Leaflet map + Chart.js) | Works, fed by `/latest` and `/readings/<node>`. |
| Enclosure CAD | Done, parametric, STL + STEP exported. |
| ESP32 firmware | **Not written yet.** The map is currently fed by `backend/test_sender.py`, which posts fake readings. |
| Nodes deployed | 0 of 3. |

So: the whole software side is real and running, the hardware side is designed
but not yet built and flashed.

---

## The three nodes

| Node | Where | Why there |
|------|-------|-----------|
| 1 | City center | Dense residential, narrow streets, not much wind |
| 2 | Periphery | Heavy traffic all day |
| 3 | Beach | Sea air, should be the clean reference |

> **TODO:** replace "City center" / "Periphery" / "Beach" with the actual
> streets or neighbourhoods, and say who is hosting each node (your balcony? a
> friend's window?). Reviewers care that these are real places.

Node 3 sits in constant marine humidity. The PMS5003 counts particles
optically, and above roughly 70 % RH the water on the particles makes them read
bigger than they are — so that node's PM values get corrected using the
humidity from its own BME280 before being stored.

---

## Hardware (per node)

Everything hangs off one ESP32. Four devices share the I2C bus, the particulate
sensor talks UART.

| Component | What it gives | Interface |
|-----------|---------------|-----------|
| ESP32 DevKit (USB-C) | MCU + WiFi | — |
| PMS5003 | PM1.0 / PM2.5 / PM10 in µg/m³ | UART, needs 5 V |
| BME280 | Temperature, humidity, pressure | I2C `0x76` |
| SCD41 | CO₂ in ppm (real NDIR, not estimated) | I2C `0x62` |
| SGP30 | VOC index | I2C `0x58` |
| 0.96" OLED | Shows the readings on the box itself | I2C `0x3C` |
| 5 V / 2 A USB-C supply | Power | — |

Full list with prices and suppliers: [`Hardware/BOM.csv`](Hardware/BOM.csv).

**Note on the two gas sensors:** the SCD41 is the one that measures CO₂
properly. The SGP30 is only there for VOC — its "eCO₂" output is an estimate
derived from VOC and is not used.

## Wiring

| Connection | ESP32 pin |
|------------|-----------|
| SDA (BME280, SCD41, SGP30, OLED) | GPIO21 |
| SCL (BME280, SCD41, SGP30, OLED) | GPIO22 |
| PMS5003 TX → ESP32 | GPIO16 (RX2) |
| PMS5003 RX → ESP32 | GPIO17 (TX2) |
| BME280 / SGP30 / OLED VCC | 3V3 |
| PMS5003 VCC, SCD41 VDD | 5 V (VIN) |
| Everything GND | GND |

Diagram: [`Hardware/CAD/circuit_image.svg`](Hardware/CAD/circuit_image.svg)

---

## Enclosure

A commercial IP65 box (150 × 110 × 70 mm) with three printed parts inside it:
a tray that holds the boards, a bezel for the OLED, and a duct that feeds
outside air to the PMS5003.

Everything lives in [`Hardware/CAD/`](Hardware/CAD):

| File | What it is |
|------|-----------|
| `valencia_air_enclosure.py` | **Source.** CadQuery script, all dimensions parametric at the top. |
| `mounting_plate.stl` | Print this — interior tray |
| `oled_bezel.stl` | Print this — display frame |
| `pms_duct.stl` | Print this — air duct |
| `valencia_air_node.step` | All three parts in one STEP, positioned as they sit in the box |

To regenerate the STL and STEP files after changing a dimension:

```bash
pip install cadquery
python Hardware/CAD/valencia_air_enclosure.py
```

The parameters marked `[VERIFICAR]` in the script are the ones I could not
confirm against a datasheet — measure your own modules with calipers before
printing, generic boards vary between batches.

The renders in [`Hardware/Images/`](Hardware/Images) are the earlier Tinkercad
mockup, kept only to show how the layout started. The CadQuery script is the
real design.

---

## Assembly

Step by step build instructions, around 2 h per node:
**[`Hardware/ASSEMBLY.md`](Hardware/ASSEMBLY.md)**

---

## Software

### Backend — `backend/`

Flask + SQLite. One table, `readings`, one row per measurement.

```bash
cd backend
pip install flask flask-cors requests
python init_db.py        # creates readings.db
python app.py            # serves on :5000
```

| Route | Method | Does |
|-------|--------|------|
| `/` | GET | Serves the map |
| `/data` | POST | A node sends a reading (JSON) |
| `/readings` | GET | Everything |
| `/latest` | GET | Last reading of each node — this is what the map markers use |
| `/readings/<node>` | GET | History of one node, for the charts |

With no hardware built yet, you can fill the database with fake readings:

```bash
python backend/test_sender.py
```

### Frontend — `frontend/index.html`

One HTML file. Leaflet for the map, Chart.js for the history panel that opens
when you click a node. No build step, no framework.

### Firmware — not written yet

Planned: Arduino on the ESP32, using `Adafruit_BME280`, `Adafruit_SGP30`,
`Sensirion SCD4x`, `PMS` and `Adafruit_SSD1306`, POSTing JSON to `/data` in the
same shape `test_sender.py` uses.

---

## What's left

- [ ] Write the ESP32 firmware
- [ ] Print the three parts and build node 1
- [ ] Find hosts for nodes 2 and 3
- [ ] Deploy and let it run
