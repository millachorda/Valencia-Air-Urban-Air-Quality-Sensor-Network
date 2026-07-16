# Assembly Instructions — Valencia Air Node

Approximate build time: ~2 h per node (plus print time and silicone cure).
All three nodes are identical.

---

## 0. Parts and tools

**From the BOM:** ESP32 DevKit, PMS5003 + JST cable, SCD41, SGP30, BME280,
OLED, IP65 enclosure, USB-C PSU, Dupont wires, PTFE membrane, neutral silicone.

**3D printed** (see `Hardware/CAD/`, PLA or PETG, 0.2 mm layers, 30% infill —
PETG preferred for the coastal node, it handles UV and heat better):
- `mounting_plate.step` — interior tray
- `oled_bezel.step` — display frame
- `pms_duct.step` — PMS5003 air duct

**Tools:** soldering iron, 20 mm hole saw (included with the CPROSP box),
3 mm drill bit, screwdriver, calipers, multimeter, zip ties.

---

## 1. Verify dimensions before printing

The CAD is parametric. Measure your actual modules with calipers and update the
`[VERIFICAR]` parameters at the top of `valencia_air_enclosure.py`, then re-run
it. Generic modules vary between batches — do not assume the defaults fit.

```bash
pip install cadquery
python valencia_air_enclosure.py
```

---

## 2. Solder headers

Solder the pin headers to the SCD41, SGP30 and BME280. Joints must be shiny and
cone-shaped against the pad. A cold joint (dull, blobby) reads as a dead module
and is very hard to diagnose later.

---

## 3. Bench test before enclosing

Wire everything on the breadboard first, per `Hardware/wiring_diagram.png`:

| From | To |
|------|-----|
| SCD41 VDD | ESP32 VIN (5 V) |
| SGP30 VIN / BME280 VIN / OLED VCC | ESP32 3V3 |
| PMS5003 VCC | ESP32 VIN (5 V) |
| All GND | ESP32 GND |
| All SDA | GPIO21 |
| All SCL | GPIO22 |
| PMS5003 TX | GPIO16 (RX2) |
| PMS5003 RX | GPIO17 (TX2) |
| PMS5003 SET / RST | leave unconnected |

Flash the firmware and open the serial monitor at 115200 baud. The I2C scanner
must report **four devices**: `0x3C`, `0x58`, `0x62`, `0x76`. Do not proceed
until all four appear — diagnosing a missing sensor inside a sealed box is
significantly harder.

Sanity checks: SCD41 should read ~420 ppm in open air and climb above 1000 ppm
if you breathe near it. The PMS5003 fan must be audible.

---

## 4. Drill the enclosure

**Bottom face** (ports face **down** so rain cannot enter):
- 2 holes ⌀12 mm, 26 mm apart, aligned with the PMS5003 inlet and outlet.

**Lid:**
- Rectangular window 24 × 14 mm for the OLED.
- 4 holes ⌀3 mm for the bezel screws.

**Side face:**
- 1 gland for the USB-C power cable.
- 1 gland for the BME280 cable (see step 6).

---

## 5. Mount the tray

1. Screw the ESP32 onto its four posts (M3 self-tapping).
2. Screw the SCD41 and SGP30 onto their posts (M2.5).
3. Seat the PMS5003 inside its rim and secure it with two zip ties through the
   slots.
4. Screw the tray to the enclosure bosses (M3).

---

## 6. Mount the BME280 OUTSIDE the box

This is not optional. Inside a closed enclosure the BME280 measures the box's
own temperature, not ambient air — under direct sun that reads up to 10 °C high,
which corrupts the humidity correction applied to the PM readings at Node 3.

Run its 4 wires out through a cable gland and mount it in shade under the box,
in a small vented radiation shield. Seal the gland with neutral silicone.

---

## 7. Air duct

1. Glue `pms_duct` to the inside of the bottom face with neutral silicone, tubes
   aligned with the two drilled holes.
2. Press one PTFE membrane disc into each pocket on the outer face.
3. **Seal the perimeter between the PMS5003 and the duct.** If air can leak
   around it, the sensor recirculates its own exhaust and measures the same air
   repeatedly instead of the atmosphere.

---

## 8. OLED window

1. Cut a 30 × 20 mm piece of clear polycarbonate or acrylic.
2. Silicone it over the window opening **from the inside**.
3. Seat the OLED PCB in the bezel pocket and screw the bezel to the lid.

The window is **sealed**. It is not a vent — all airflow goes through the duct.

---

## 9. Final assembly

1. Route and secure all cables away from the PMS5003 fan.
2. Tighten every gland.
3. Apply neutral silicone to all penetrations and let it cure **24 h before
   deployment**.
4. Close the lid with the four original screws.

---

## 10. Deployment

Mount with the air duct facing down, ideally under an eave or small visor,
1.5–3 m above ground, away from direct exhaust sources. Confirm WiFi RSSI is
better than −75 dBm at the final location — the serial log prints it at boot.

**Ingress rating note:** drilling the air duct means the enclosure is no longer
strictly IP65. With downward-facing ports and PTFE membranes it is effectively
rain-protected (~IP54). This is standard practice for outdoor air quality
stations — a particulate sensor in a truly sealed box measures nothing.
