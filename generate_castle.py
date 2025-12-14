#!/usr/bin/env python3
"""
CASTLE GENERATOR v12 - Cinematic Siege
=======================================
The Final Cut:
- CINEMATIC CAMERA: Dramatic orbiting shot from gatekeeper to tactical view
- VEHICLES: Motorcycle patrol, supply carts
- TIGHTER SCALE: Action-packed layout, less empty floor
- PROPER Y-COORDS: All items ON the floor (Y=0)

Uses verified LDraw parts that render correctly.
"""

from dataclasses import dataclass
from typing import List, Tuple
import math

# ===== LDraw Units =====
STUD = 20
BRICK = 24
PLATE = 8

# ===== COLORS =====
STONE_GRAY = 7
DARK_STONE = 8
WOOD_BROWN = 6
GREEN = 2
TORCH_ORANGE = 25
DEFAULT_COLOR = 16
VEHICLE_RED = 4
VEHICLE_WHITE = 15

@dataclass
class Part:
    color: int
    x: int
    y: int
    z: int
    matrix: Tuple[int, int, int, int, int, int, int, int, int]
    part: str

IDENT = (1, 0, 0, 0, 1, 0, 0, 0, 1)
ROT_Y_90 = (0, 0, -1, 0, 1, 0, 1, 0, 0)
ROT_Y_180 = (-1, 0, 0, 0, 1, 0, 0, 0, -1)
ROT_Y_270 = (0, 0, 1, 0, 1, 0, -1, 0, 0)


def emit_parts(parts: List[Part]) -> str:
    lines = []
    for p in parts:
        a, b, c, d, e, f, g, h, i = p.matrix
        lines.append(f"1 {p.color} {p.x} {p.y} {p.z}  {a} {b} {c}  {d} {e} {f}  {g} {h} {i}  {p.part}")
    return "\n".join(lines)


# ==================== MINIFIGS ====================
DEFENDER_PARTS = [
    {"head": "3626bpaa.dat", "headgear": "30113.dat", "torso": "76382p1y.dat", 
     "hips": "3815bpba.dat", "leg_l": "3817cp6u.dat", "leg_r": "3816cp6u.dat"},
    {"head": "3626cp71.dat", "headgear": "10113.dat", "torso": "76382p8l.dat",
     "hips": "21019bpdgb.dat", "leg_l": "3817cp6u.dat", "leg_r": "3816cp6u.dat"},
]

GATEKEEPER_PARTS = {
    "head": "3626cp7i.dat", "headgear": "30561.dat", "torso": "24319pcfd.dat",
    "hips": "3815bpc39.dat", "leg_l": "3817cp6u.dat", "leg_r": "3816cp6u.dat"
}

INVADER_PARTS = [
    {"head": "3626bp56.dat", "headgear": None, "torso": "76382p0h.dat",
     "hips": "3815bpy0.dat", "leg_l": "3817cpa3.dat", "leg_r": "3816cpa3.dat"},
    {"head": "3626cp79.dat", "headgear": "11418.dat", "torso": "76382p1d.dat",
     "hips": "3815bpx1.dat", "leg_l": "3817cpdga.dat", "leg_r": "3816cpdga.dat"},
]

def add_minifig(parts: List[Part], x: int, ground_y: int, z: int,
                rotation: Tuple, minifig_parts: dict) -> None:
    c = DEFAULT_COLOR
    parts.append(Part(c, x, ground_y - 84, z, rotation, minifig_parts["head"]))
    if minifig_parts.get("headgear"):
        parts.append(Part(c, x, ground_y - 84, z, rotation, minifig_parts["headgear"]))
    parts.append(Part(c, x, ground_y - 60, z, rotation, minifig_parts["torso"]))
    parts.append(Part(c, x, ground_y - 28, z, rotation, minifig_parts["hips"]))
    parts.append(Part(c, x, ground_y - 16, z, rotation, minifig_parts["leg_l"]))
    parts.append(Part(c, x, ground_y - 16, z, rotation, minifig_parts["leg_r"]))


# ==================== VEHICLES (Y=0) ====================

def add_motorcycle(parts: List[Part], x: int, z: int, rotation: Tuple) -> None:
    """3-Wheel Motorcycle Patrol."""
    # Chassis
    parts.append(Part(VEHICLE_RED, x, 0, z, rotation, "65634.dat"))
    # Wheels (3-wheel setup)
    parts.append(Part(DEFAULT_COLOR, x, -20, z, rotation, "30187c03.dat"))
    # Windscreen
    parts.append(Part(VEHICLE_WHITE, x, -40, z - 10, rotation, "13760.dat"))

def add_supply_cart(parts: List[Part], x: int, z: int, rotation: Tuple) -> None:
    """Supply cart with crates."""
    # Base
    parts.append(Part(WOOD_BROWN, x, 0, z, rotation, "3001.dat"))  # 2x4 brick as bed
    # Wheels
    parts.append(Part(DEFAULT_COLOR, x - 20, 0, z, rotation, "30027.dat"))  # Wheel
    parts.append(Part(DEFAULT_COLOR, x + 20, 0, z, rotation, "30027.dat"))
    # Cargo
    parts.append(Part(WOOD_BROWN, x, -24, z, rotation, "3003.dat")) # Crate


# ==================== STRUCTURES (Y=0) ====================

def add_tower(parts: List[Part], cx: int, cz: int, layers: int = 6) -> int:
    offsets = [(-20, -20), (20, -20), (-20, 20), (20, 20)]
    for layer in range(layers):
        y = -layer * BRICK
        for dx, dz in offsets:
            parts.append(Part(STONE_GRAY, cx + dx, y, cz + dz, IDENT, "3003.dat"))
    return -layers * BRICK

def add_wall(parts: List[Part], x: int, z: int, layers: int, rotation: Tuple) -> None:
    for layer in range(layers):
        y = -layer * BRICK
        parts.append(Part(STONE_GRAY, x, y, z, rotation, "3001.dat"))

def add_cottage(parts: List[Part], x: int, z: int) -> None:
    # Foundation
    parts.append(Part(STONE_GRAY, x, 0, z, IDENT, "3001.dat"))
    parts.append(Part(STONE_GRAY, x, 0, z + 40, IDENT, "3001.dat"))
    # Walls
    parts.append(Part(WOOD_BROWN, x, -24, z, IDENT, "3001.dat"))
    parts.append(Part(WOOD_BROWN, x, -24, z + 40, IDENT, "3001.dat"))
    # Roof
    parts.append(Part(DARK_STONE, x, -48, z + 20, IDENT, "3020.dat"))

def add_lamppost(parts: List[Part], x: int, z: int) -> None:
    parts.append(Part(DARK_STONE, x, 0, z, IDENT, "723.dat"))

def add_well(parts: List[Part], x: int, z: int) -> None:
    parts.append(Part(STONE_GRAY, x, 0, z, IDENT, "3003.dat"))
    parts.append(Part(STONE_GRAY, x, -24, z, IDENT, "3003.dat"))


# ==================== MAIN GENERATOR ====================
def generate_castle(castle_size: int, wall_layers: int, tower_layers: int) -> Tuple[str, int]:
    parts: List[Part] = []
    
    scale = max(1, castle_size // 32)
    # Tighter scale - fill the space better
    half = (castle_size * STUD) // 2
    
    tower_inset = 60 * scale
    tower_pos = half - tower_inset
    wall_pos = half - 40 * scale
    
    # ===== FLOOR (Y=0) =====
    plate_size = 32 * STUD
    plate_count = max(1, castle_size // 32)
    for ix in range(plate_count):
        for iz in range(plate_count):
            x = int((ix - (plate_count - 1) / 2) * plate_size)
            z = int((iz - (plate_count - 1) / 2) * plate_size)
            parts.append(Part(DEFAULT_COLOR, x, 0, z, IDENT, "6099p01.dat"))
    
    # ===== STRUCTURES =====
    tower_positions = []
    for tx, tz in [(-tower_pos, -tower_pos), (tower_pos, -tower_pos),
                   (-tower_pos, tower_pos), (tower_pos, tower_pos)]:
        roof_y = add_tower(parts, tx, tz, tower_layers)
        tower_positions.append((tx, roof_y, tz))
    
    # Walls
    brick_spacing = 80
    
    # North
    x = -wall_pos + brick_spacing
    while x < wall_pos - brick_spacing // 2:
        add_wall(parts, x, -wall_pos, wall_layers, IDENT)
        x += brick_spacing
    
    # South (Gate)
    x = -wall_pos + brick_spacing
    while x < wall_pos - brick_spacing // 2:
        if abs(x) > 60:
            add_wall(parts, x, wall_pos, wall_layers, IDENT)
        x += brick_spacing
        
    # East/West
    z = -wall_pos + brick_spacing
    while z < wall_pos - brick_spacing // 2:
        add_wall(parts, wall_pos, z, wall_layers, ROT_Y_90)
        add_wall(parts, -wall_pos, z, wall_layers, ROT_Y_90)
        z += brick_spacing
    
    # ===== INTERIOR LIFE (Y=0) =====
    add_cottage(parts, -wall_pos + 100, -wall_pos + 100)
    if scale >= 2:
        add_cottage(parts, wall_pos - 140, -wall_pos + 100)
    
    add_well(parts, 0, 0)
    
    # Vehicles inside
    add_supply_cart(parts, 80, -60, ROT_Y_270)
    
    # Vehicles outside - Patrol
    add_motorcycle(parts, -120, wall_pos + 160, ROT_Y_180)  # Patrol motorcycle
    if scale >= 2:
        add_motorcycle(parts, 120, wall_pos + 160, ROT_Y_180)
    
    # Gate elements
    add_lamppost(parts, -60, wall_pos - 30)
    add_lamppost(parts, 60, wall_pos - 30)
    
    # ===== MINIFIGS =====
    wall_top_y = -wall_layers * BRICK
    
    # Defenders
    for x in [-120, -40, 40, 120]:
        if abs(x) < wall_pos:
            add_minifig(parts, x, wall_top_y, -wall_pos, ROT_Y_180, DEFENDER_PARTS[0])
            
    # Gatekeeper Hero
    add_minifig(parts, 0, 0, wall_pos - 40, ROT_Y_180, GATEKEEPER_PARTS)
    
    # Invaders
    invader_positions = [(-60, 100), (0, 120), (60, 100), (-40, 160), (40, 160)]
    for x, z_off in invader_positions:
        add_minifig(parts, x, 0, wall_pos + z_off, IDENT, INVADER_PARTS[0])
        
    
    # ===== MENTO CINEMATIC =====
    cam_dist = half * 2.5
    tower_top = -tower_layers * BRICK
    
    header = f"""0 FILE CASTLE_{castle_size}x{castle_size}.mpd
0 Name: Cinematic Siege - {castle_size}x{castle_size}
0 Author: WAG Castle Generator v12
0 !LDRAW_ORG Model
0 !LICENCE Redistributable under CCAL version 2.0
0 BFC CERTIFY CCW

0 // ============================================================
0 // DRAMATIC LIGHTING
0 // ============================================================
0 !MENTO LIGHT "Sunset Key" TYPE SUN POS {-cam_dist} {tower_top*2} {cam_dist} TGT 0 0 0 COLOR #FF9944 INTENSITY 1.1 SHADOWS TRUE
0 !MENTO LIGHT "Blue Fill" TYPE SUN POS {cam_dist} {tower_top*2} {-cam_dist} TGT 0 0 0 COLOR #446688 INTENSITY 0.4 SHADOWS FALSE
0 !MENTO LIGHT "Gate Spot" TYPE SPOT POS 0 {tower_top} {wall_pos+100} TGT 0 0 {wall_pos-40} CUTOFF 45 COLOR #FFAA55 INTENSITY 1.5

0 // ============================================================
0 // CINEMATIC ORBIT SHOT
0 // ============================================================

0 // 1. GATEKEEPER HERO (Low angle, dramatic)
0 !MENTO SHOT "The Gatekeeper" POS 0 -20 {wall_pos + 80} TGT 0 -60 {wall_pos - 40} LENS 85 DURATION 6

0 // 2. REVEAL INVADERS (Pull back and up)
0 !MENTO SHOT "The Threat" POS {-100} -100 {wall_pos + 250} TGT 0 -40 {wall_pos + 100} LENS 50 DURATION 5

0 // 3. ORBIT - WEST SIDE (Circling the action)
0 !MENTO SHOT "Orbit West" POS {-cam_dist} -150 0 TGT 0 -40 0 LENS 60 DURATION 5

0 // 4. ORBIT - NORTH (Defenders on wall)
0 !MENTO SHOT "Orbit North" POS 0 -200 {-cam_dist} TGT 0 {wall_top_y} {-wall_pos} LENS 70 DURATION 5

0 // 5. ORBIT - EAST (Courtyard activity)
0 !MENTO SHOT "Orbit East" POS {cam_dist} -150 0 TGT 0 -40 0 LENS 60 DURATION 5

0 // 6. RETURN TO GATE (Full circle complete)
0 !MENTO SHOT "Full Circle" POS {cam_dist/3} -100 {wall_pos + 150} TGT 0 -40 {wall_pos} LENS 50 DURATION 6

0 // ============================================================
0 // GEOMETRY
0 // ============================================================

0 STEP
"""
    content = header + emit_parts(parts) + "\n\n0 NOFILE\n"
    return content, len(parts)


def main():
    configs = [
        ("CASTLE_SMALL.mpd", 32, 4, 7),
        ("CASTLE_MEDIUM.mpd", 48, 5, 9),
        ("CASTLE_LARGE.mpd", 64, 6, 11),
    ]
    
    print("Generating castles v12 (Cinematic Siege)...\n")
    
    for filename, castle_size, wall_layers, tower_layers in configs:
        content, part_count = generate_castle(castle_size, wall_layers, tower_layers)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        size_kb = len(content.encode()) / 1024
        
        print(f"✓ {filename}")
        print(f"  {castle_size}x{castle_size} studs | {part_count} parts")
    
    print("\nDONE: Dramatic camera, vehicles (motorcycle!), optimized scale.")

if __name__ == "__main__":
    main()
