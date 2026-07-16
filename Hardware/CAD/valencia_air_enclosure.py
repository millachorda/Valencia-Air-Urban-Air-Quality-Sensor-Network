import cadquery as cq

# =====================================================================
# PARAMETROS
# =====================================================================

# --- Caja comercial CPROSP IP65 ---------------------------------------
BOX_L, BOX_W, BOX_H = 150.0, 110.0, 70.0   # exterior nominal
WALL = 2.5                                  # espesor pared [VERIFICAR]
PLATE_L = 132.0                             # bandeja: holgura de ~4mm/lado
PLATE_W = 92.0
PLATE_T = 3.0                               # espesor bandeja

# Tornillos de la bandeja a los bosses de la caja [VERIFICAR con calibre]
BOSS_DX = 118.0        # separacion X entre bosses
BOSS_DY = 78.0         # separacion Y entre bosses
BOSS_HOLE_D = 3.4      # paso M3

# --- ESP32 DevKit V1 38 pines [VERIFICAR] -----------------------------
ESP_L, ESP_W = 55.0, 28.0
ESP_HOLE_DX = 48.0     # separacion agujeros de montaje en X
ESP_HOLE_DY = 21.5     # separacion en Y
ESP_POST_H = 8.0       # altura del pilar: deja pasar los pines por debajo
ESP_POST_D = 6.0
ESP_HOLE_D = 2.6       # M3 autorroscante en plastico
ESP_POS = (-32.0, 18.0)

# --- PMS5003 (datasheet Plantower) ------------------------------------
PMS_L, PMS_W, PMS_H = 50.0, 38.0, 21.0
PMS_POS = (34.0, -20.0)          # cerca del borde inferior de la caja
PMS_TIE_SLOT_W = 4.0             # ranuras para brida
PMS_TIE_SLOT_L = 12.0
# Bocas de aire: separacion entre centros de entrada y salida [VERIFICAR]
PMS_PORT_SPACING = 26.0
PMS_PORT_D = 11.0

# --- Modulos I2C pequenos ---------------------------------------------
SCD41_L, SCD41_W = 21.6, 13.4    # dato de fabricante (Hailege)
BME280_L, BME280_W = 13.0, 10.5  # [VERIFICAR]
SGP30_L, SGP30_W = 20.0, 15.0    # [VERIFICAR]
SMALL_POST_H = 6.0
SMALL_POST_D = 5.0
SMALL_HOLE_D = 2.1               # M2.5 autorroscante

SCD41_POS = (34.0, 22.0)
SGP30_POS = (5.0, 22.0)
# El BME280 NO va en la bandeja: va fuera, a la sombra, via prensaestopas.
# Ver ASSEMBLY.md. Se deja pilar de reserva por si se monta interior.
BME280_POS = (5.0, -8.0)

# --- OLED 0.96" -------------------------------------------------------
OLED_PCB_L, OLED_PCB_W = 27.0, 27.0     # [VERIFICAR]
OLED_HOLE_DX = 23.0
OLED_HOLE_DY = 23.0
OLED_WINDOW_L, OLED_WINDOW_W = 24.0, 14.0   # area visible del cristal
BEZEL_L, BEZEL_W, BEZEL_T = 36.0, 36.0, 4.0
BEZEL_HOLE_D = 2.1

# --- Conducto PMS5003 -------------------------------------------------
DUCT_FLANGE_L, DUCT_FLANGE_W, DUCT_FLANGE_T = 44.0, 24.0, 3.0
DUCT_TUBE_H = 8.0
DUCT_TUBE_OD = 14.0
DUCT_MEMBRANE_POCKET_D = 16.0
DUCT_MEMBRANE_POCKET_T = 1.0


# =====================================================================
# UTILIDADES
# =====================================================================

def add_posts(part, positions, post_d, post_h, hole_d, base_z):
    """Anade pilares cilindricos con agujero central sobre la bandeja."""
    for (x, y) in positions:
        post = (
            cq.Workplane("XY")
            .center(x, y)
            .circle(post_d / 2.0)
            .extrude(post_h)
            .translate((0, 0, base_z))
        )
        part = part.union(post)
    for (x, y) in positions:
        part = (
            part.faces(">Z").workplane(origin=(0, 0, base_z + post_h))
            .center(x, y)
            .hole(hole_d, post_h + 1.0)
        )
    return part


def rect_hole_positions(center, dx, dy):
    cx, cy = center
    return [
        (cx - dx / 2.0, cy - dy / 2.0),
        (cx + dx / 2.0, cy - dy / 2.0),
        (cx - dx / 2.0, cy + dy / 2.0),
        (cx + dx / 2.0, cy + dy / 2.0),
    ]


# =====================================================================
# PIEZA 1 - BANDEJA DE MONTAJE
# =====================================================================

def make_mounting_plate():
    plate = (
        cq.Workplane("XY")
        .box(PLATE_L, PLATE_W, PLATE_T, centered=(True, True, False))
        .edges("|Z").fillet(4.0)
    )

    # Taladros de sujecion a la caja
    plate = (
        plate.faces(">Z").workplane()
        .rect(BOSS_DX, BOSS_DY, forConstruction=True)
        .vertices()
        .hole(BOSS_HOLE_D)
    )

    # Pilares ESP32
    plate = add_posts(
        plate,
        rect_hole_positions(ESP_POS, ESP_HOLE_DX, ESP_HOLE_DY),
        ESP_POST_D, ESP_POST_H, ESP_HOLE_D, PLATE_T,
    )

    # Pilares modulos I2C (un pilar por esquina util del modulo)
    for pos, (l, w) in [
        (SCD41_POS, (SCD41_L, SCD41_W)),
        (SGP30_POS, (SGP30_L, SGP30_W)),
        (BME280_POS, (BME280_L, BME280_W)),
    ]:
        pts = rect_hole_positions(pos, l - 5.0, w - 5.0)
        plate = add_posts(plate, [pts[0], pts[3]], SMALL_POST_D,
                          SMALL_POST_H, SMALL_HOLE_D, PLATE_T)

    # Asiento del PMS5003: reborde de posicionamiento + ranuras para bridas
    px, py = PMS_POS
    rim = (
        cq.Workplane("XY")
        .center(px, py)
        .rect(PMS_L + 2.4, PMS_W + 2.4)
        .extrude(2.5)
        .cut(
            cq.Workplane("XY").center(px, py)
            .rect(PMS_L + 0.4, PMS_W + 0.4).extrude(2.5)
        )
        .translate((0, 0, PLATE_T))
    )
    plate = plate.union(rim)

    for sy in (py - PMS_W / 2.0 - 4.0, py + PMS_W / 2.0 + 4.0):
        for sx in (px - 14.0, px + 14.0):
            slot = (
                cq.Workplane("XY").center(sx, sy)
                .slot2D(PMS_TIE_SLOT_L, PMS_TIE_SLOT_W, 0)
                .extrude(PLATE_T + 1.0)
                .translate((0, 0, -0.5))
            )
            plate = plate.cut(slot)

    # Aligeramiento / paso de cables
    for cx in (-8.0, 12.0):
        vent = (
            cq.Workplane("XY").center(cx, -32.0)
            .slot2D(40.0, 6.0, 0)
            .extrude(PLATE_T + 2.0)
            .translate((0, 0, -1.0))
        )
        plate = plate.cut(vent)

    return plate


# =====================================================================
# PIEZA 2 - BISEL OLED (ventana SELLADA)
# =====================================================================

def make_oled_bezel():
    bezel = (
        cq.Workplane("XY")
        .box(BEZEL_L, BEZEL_W, BEZEL_T, centered=(True, True, False))
        .edges("|Z").fillet(3.0)
    )

    # Rebaje trasero donde encaja el PCB de la OLED
    pocket = (
        cq.Workplane("XY")
        .rect(OLED_PCB_L + 0.4, OLED_PCB_W + 0.4)
        .extrude(1.6)
        .translate((0, 0, BEZEL_T - 1.6))
    )
    bezel = bezel.cut(pocket)

    # Ventana de vision
    window = (
        cq.Workplane("XY")
        .rect(OLED_WINDOW_L, OLED_WINDOW_W)
        .extrude(BEZEL_T + 2.0)
        .translate((0, 0, -1.0))
    )
    bezel = bezel.cut(window)

    # Agujeros de fijacion del PCB
    bezel = (
        bezel.faces(">Z").workplane()
        .rect(OLED_HOLE_DX, OLED_HOLE_DY, forConstruction=True)
        .vertices()
        .hole(BEZEL_HOLE_D)
    )

    # Agujeros para atornillar el bisel a la tapa
    bezel = (
        bezel.faces(">Z").workplane()
        .rect(BEZEL_L - 5.0, BEZEL_W - 5.0, forConstruction=True)
        .vertices()
        .hole(BOSS_HOLE_D)
    )

    return bezel


# =====================================================================
# PIEZA 3 - CONDUCTO PMS5003
# =====================================================================

def make_pms_duct():
    flange = (
        cq.Workplane("XY")
        .box(DUCT_FLANGE_L, DUCT_FLANGE_W, DUCT_FLANGE_T,
             centered=(True, True, False))
        .edges("|Z").fillet(3.0)
    )

    for sx in (-PMS_PORT_SPACING / 2.0, PMS_PORT_SPACING / 2.0):
        tube = (
            cq.Workplane("XY").center(sx, 0)
            .circle(DUCT_TUBE_OD / 2.0)
            .extrude(DUCT_TUBE_H)
            .translate((0, 0, DUCT_FLANGE_T))
        )
        flange = flange.union(tube)

    # Perforacion pasante de cada boca
    for sx in (-PMS_PORT_SPACING / 2.0, PMS_PORT_SPACING / 2.0):
        bore = (
            cq.Workplane("XY").center(sx, 0)
            .circle(PMS_PORT_D / 2.0)
            .extrude(DUCT_FLANGE_T + DUCT_TUBE_H + 2.0)
            .translate((0, 0, -1.0))
        )
        flange = flange.cut(bore)

    # Alojamiento de la membrana PTFE en la cara exterior
    for sx in (-PMS_PORT_SPACING / 2.0, PMS_PORT_SPACING / 2.0):
        pocket = (
            cq.Workplane("XY").center(sx, 0)
            .circle(DUCT_MEMBRANE_POCKET_D / 2.0)
            .extrude(DUCT_MEMBRANE_POCKET_T)
        )
        flange = flange.cut(pocket)

    return flange


# =====================================================================
# EXPORTACION
# =====================================================================

if __name__ == "__main__":
    plate = make_mounting_plate()
    bezel = make_oled_bezel()
    duct = make_pms_duct()

    # STL individuales (para imprimir)
    cq.exporters.export(plate, "mounting_plate.stl")
    cq.exporters.export(bezel, "oled_bezel.stl")
    cq.exporters.export(duct, "pms_duct.stl")

    # UN SOLO STEP con las tres piezas como cuerpos independientes y
    # nombrados, colocadas en su posicion relativa dentro de la caja.
    asm = cq.Assembly(name="valencia_air_node")
    asm.add(plate, name="mounting_plate",
            color=cq.Color("steelblue"))
    asm.add(bezel, name="oled_bezel",
            loc=cq.Location(cq.Vector(-45.0, 30.0, 40.0)),
            color=cq.Color("gray"))
    asm.add(duct, name="pms_duct",
            loc=cq.Location(cq.Vector(PMS_POS[0], PMS_POS[1], -6.0),
                            cq.Vector(1, 0, 0), 180),
            color=cq.Color("darkorange"))
    asm.save("valencia_air_node.step")

    print("Exportado:")
    print("  valencia_air_node.step   <- las 3 piezas en un unico STEP")
    for f in ["mounting_plate", "oled_bezel", "pms_duct"]:
        print(f"  {f}.stl")
