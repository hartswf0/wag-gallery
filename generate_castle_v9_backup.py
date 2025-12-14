#!/usr/bin/env python3
"""
CASTLE GENERATOR v9 - Rich Siege Scene
=======================================
Enhanced with:
- MORE SOLDIERS: 6+ defenders, 6+ invaders
- RICH PLACEMAKING: Containers, trees, lampposts, barrels
- MOOD LIGHTING: Sunset atmosphere
- NARRATIVE: Clear roles and positions

Uses ONLY verified LDraw parts that render correctly.
Ground level is Y=0, UP is -Y direction.
"""

from dataclasses import dataclass
from typing import List, Tuple

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


# ==================== VERIFIED MINIFIG PARTS ====================
# Y positions: Head=-84, Headgear=-84, Torso=-60, Hips=-28, Legs=-16

DEFENDER_PARTS = [
    # Type 1 - Standard guard
    {"head": "3626bpaa.dat", "headgear": "30113.dat", "torso": "76382p1y.dat", 
     "hips": "3815bpba.dat", "leg_l": "3817cp6u.dat", "leg_r": "3816cp6u.dat"},
    # Type 2 - Knight
    {"head": "3626cp71.dat", "headgear": "10113.dat", "torso": "76382p8l.dat",
     "hips": "21019bpdgb.dat", "leg_l": "3817cp6u.dat", "leg_r": "3816cp6u.dat"},
    # Type 3 - Commander (wookiee head pattern, royal guard headdress)
    {"head": "30483.dat", "headgear": "30561.dat", "torso": "76382p1q.dat",
     "hips": "3815bpm2.dat", "leg_l": "3817cpy2.dat", "leg_r": "3816cpy2.dat"},
]

INVADER_PARTS = [
    # Type 1 - Raider
    {"head": "3626bp56.dat", "headgear": None, "torso": "76382p0h.dat",
     "hips": "3815bpy0.dat", "leg_l": "3817cpa3.dat", "leg_r": "3816cpa3.dat"},
    # Type 2 - Scout
    {"head": "3626cp79.dat", "headgear": "11418.dat", "torso": "76382p1d.dat",
     "hips": "3815bpx1.dat", "leg_l": "3817cpdga.dat", "leg_r": "3816cpdga.dat"},
    # Type 3 - Warrior
    {"head": "3626cp71.dat", "headgear": None, "torso": "76382p8l.dat",
     "hips": "21019bpdgb.dat", "leg_l": "3817cp6u.dat", "leg_r": "3816cp6u.dat"},
]

GATEKEEPER_PARTS = {
    "head": "3626cp7i.dat", "headgear": "30561.dat", "torso": "24319pcfd.dat",
    "hips": "3815bpc39.dat", "leg_l": "3817cp6u.dat", "leg_r": "3816cp6u.dat"
}


def add_minifig(parts: List[Part], x: int, ground_y: int, z: int,
                rotation: Tuple, minifig_parts: dict) -> None:
    """Add minifig at position. ground_y is the surface Y (0 for floor)."""
    c = DEFAULT_COLOR
    
    parts.append(Part(c, x, ground_y - 84, z, rotation, minifig_parts["head"]))
    if minifig_parts.get("headgear"):
        parts.append(Part(c, x, ground_y - 84, z, rotation, minifig_parts["headgear"]))
    parts.append(Part(c, x, ground_y - 60, z, rotation, minifig_parts["torso"]))
    parts.append(Part(c, x, ground_y - 28, z, rotation, minifig_parts["hips"]))
    parts.append(Part(c, x, ground_y - 16, z, rotation, minifig_parts["leg_l"]))
    parts.append(Part(c, x, ground_y - 16, z, rotation, minifig_parts["leg_r"]))


# ==================== STRUCTURE ====================
def add_tower(parts: List[Part], cx: int, cz: int, layers: int = 6) -> int:
    """Corner tower using 2x2 bricks."""
    offsets = [(-20, -20), (20, -20), (-20, 20), (20, 20)]
    for layer in range(layers):
        y = -layer * BRICK
        for dx, dz in offsets:
            parts.append(Part(STONE_GRAY, cx + dx, y, cz + dz, IDENT, "3003.dat"))
    return -layers * BRICK


def add_wall(parts: List[Part], x: int, z: int, layers: int, rotation: Tuple) -> None:
    """Wall segment using 2x4 bricks."""
    for layer in range(layers):
        parts.append(Part(STONE_GRAY, x, -layer * BRICK, z, rotation, "3001.dat"))


def add_keep(parts: List[Part], cx: int, cz: int, layers: int) -> int:
    """Central keep using 2x2 bricks."""
    for layer in range(layers):
        parts.append(Part(DARK_STONE, cx, -layer * BRICK, cz, IDENT, "3003.dat"))
    return -layers * BRICK


# ==================== PLACEMAKING ====================
def add_container_small(parts: List[Part], x: int, z: int) -> None:
    """Small crate using 2x2 brick."""
    parts.append(Part(WOOD_BROWN, x, 0, z, IDENT, "3003.dat"))


def add_container_large(parts: List[Part], x: int, z: int) -> None:
    """Large crate using 2x4 brick."""
    parts.append(Part(WOOD_BROWN, x, 0, z, IDENT, "3001.dat"))


def add_tree(parts: List[Part], x: int, z: int) -> None:
    """Tree using plant bush part."""
    parts.append(Part(GREEN, x, -8, z, IDENT, "6064b.dat"))


def add_lamppost(parts: List[Part], x: int, z: int) -> None:
    """Lamppost using 1x1 bricks stacked."""
    parts.append(Part(DARK_STONE, x, 0, z, IDENT, "3005.dat"))
    parts.append(Part(DARK_STONE, x, -24, z, IDENT, "3005.dat"))
    parts.append(Part(DARK_STONE, x, -48, z, IDENT, "3005.dat"))
    parts.append(Part(TORCH_ORANGE, x, -56, z, IDENT, "3024.dat"))


def add_barrel(parts: List[Part], x: int, z: int) -> None:
    """Barrel using cylinder-ish 2x2 round brick."""
    parts.append(Part(WOOD_BROWN, x, 0, z, IDENT, "3941.dat"))


def add_door_frame(parts: List[Part], x: int, z: int) -> None:
    """Door frame using 1x1 bricks."""
    parts.append(Part(WOOD_BROWN, x - 20, 0, z, IDENT, "3005.dat"))
    parts.append(Part(WOOD_BROWN, x + 20, 0, z, IDENT, "3005.dat"))
    parts.append(Part(WOOD_BROWN, x - 20, -24, z, IDENT, "3005.dat"))
    parts.append(Part(WOOD_BROWN, x + 20, -24, z, IDENT, "3005.dat"))
    parts.append(Part(WOOD_BROWN, x, -48, z, IDENT, "3622.dat"))  # 1x3 brick as lintel


# ==================== MAIN GENERATOR ====================
def generate_castle(castle_size: int, wall_layers: int, tower_layers: int,
                    has_keep: bool, keep_layers: int) -> Tuple[str, int]:
    parts: List[Part] = []
    
    scale = max(1, castle_size // 32)
    half = (castle_size * STUD) // 2
    
    tower_inset = 60 * scale
    tower_pos = half - tower_inset
    wall_pos = half - 40 * scale
    
    # ===== FLOOR =====
    plate_size = 32 * STUD
    plate_count = max(1, castle_size // 32)
    
    for ix in range(plate_count):
        for iz in range(plate_count):
            x = int((ix - (plate_count - 1) / 2) * plate_size)
            z = int((iz - (plate_count - 1) / 2) * plate_size)
            parts.append(Part(DEFAULT_COLOR, x, 0, z, IDENT, "6099p01.dat"))
    
    # ===== CORNER TOWERS =====
    tower_positions = []
    for tx, tz in [(-tower_pos, -tower_pos), (tower_pos, -tower_pos),
                   (-tower_pos, tower_pos), (tower_pos, tower_pos)]:
        roof_y = add_tower(parts, tx, tz, tower_layers)
        tower_positions.append((tx, roof_y, tz))
    
    # ===== WALLS =====
    brick_spacing = 80
    
    # North wall (solid)
    x = -wall_pos + brick_spacing
    while x < wall_pos - brick_spacing // 2:
        add_wall(parts, x, -wall_pos, wall_layers, IDENT)
        x += brick_spacing
    
    # South wall (gate opening in center)
    x = -wall_pos + brick_spacing
    while x < wall_pos - brick_spacing // 2:
        if abs(x) > 60:
            add_wall(parts, x, wall_pos, wall_layers, IDENT)
        x += brick_spacing
    
    # East and West walls
    z = -wall_pos + brick_spacing
    while z < wall_pos - brick_spacing // 2:
        add_wall(parts, wall_pos, z, wall_layers, ROT_Y_90)
        add_wall(parts, -wall_pos, z, wall_layers, ROT_Y_90)
        z += brick_spacing
    
    # ===== KEEP =====
    keep_roof_y = 0
    if has_keep:
        keep_roof_y = add_keep(parts, 0, 0, keep_layers)
    
    # ===== GATE DOOR =====
    add_door_frame(parts, 0, wall_pos - 10)
    
    # ===== PLACEMAKING =====
    # Containers in courtyard corners
    add_container_large(parts, -80, -80)
    add_container_small(parts, -60, -100)
    add_container_large(parts, 80, -80)
    add_container_small(parts, 100, -100)
    
    # Barrels near gate
    add_barrel(parts, -50, wall_pos - 60)
    add_barrel(parts, 50, wall_pos - 60)
    
    # Lampposts at gate
    add_lamppost(parts, -60, wall_pos - 30)
    add_lamppost(parts, 60, wall_pos - 30)
    
    # Trees outside castle
    add_tree(parts, -tower_pos - 40, tower_pos + 80)
    add_tree(parts, tower_pos + 40, tower_pos + 80)
    add_tree(parts, -tower_pos - 60, -tower_pos - 40)
    
    # ===============================================
    # MINIFIGS - THE SIEGE
    # ===============================================
    wall_top_y = -wall_layers * BRICK
    
    # DEFENDERS - On north wall (6-8 soldiers)
    defender_positions = [
        (-160, wall_top_y, -wall_pos),
        (-100, wall_top_y, -wall_pos),
        (-40, wall_top_y, -wall_pos),
        (40, wall_top_y, -wall_pos),
        (100, wall_top_y, -wall_pos),
        (160, wall_top_y, -wall_pos),
    ]
    for i, (x, y, z) in enumerate(defender_positions[:min(6, scale * 2 + 2)]):
        parts_def = DEFENDER_PARTS[i % len(DEFENDER_PARTS)]
        add_minifig(parts, x, y, z, ROT_Y_180, parts_def)
    
    # Defenders on tower tops (2)
    for i, (tx, ty, tz) in enumerate(tower_positions[:2]):
        parts_def = DEFENDER_PARTS[(i + 1) % len(DEFENDER_PARTS)]
        add_minifig(parts, tx, ty, tz, ROT_Y_180, parts_def)
    
    # GATEKEEPERS - At the gate (2 flanking)
    add_minifig(parts, -30, 0, wall_pos - 60, ROT_Y_180, GATEKEEPER_PARTS)
    add_minifig(parts, 30, 0, wall_pos - 60, ROT_Y_180, GATEKEEPER_PARTS)
    
    # INVADERS - Outside south gate (6-8 attackers)
    invader_positions = [
        (-80, 0, wall_pos + 100),
        (-40, 0, wall_pos + 80),
        (0, 0, wall_pos + 120),
        (40, 0, wall_pos + 80),
        (80, 0, wall_pos + 100),
        (-60, 0, wall_pos + 160),
        (0, 0, wall_pos + 180),
        (60, 0, wall_pos + 160),
    ]
    for i, (x, y, z) in enumerate(invader_positions[:min(8, scale * 2 + 4)]):
        parts_inv = INVADER_PARTS[i % len(INVADER_PARTS)]
        add_minifig(parts, x, y, z, IDENT, parts_inv)  # Facing castle
    
    # ===============================================
    # MENTO LIGHTING & CAMERA
    # ===============================================
    cam_distance = half * 2
    tower_top = -tower_layers * BRICK
    
    header = f"""0 FILE CASTLE_{castle_size}x{castle_size}.mpd
0 Name: Castle Siege - {castle_size}x{castle_size}
0 Author: WAG Castle Generator v9
0 !LDRAW_ORG Model
0 !LICENCE Redistributable under CCAL version 2.0
0 BFC CERTIFY CCW

0 // ============================================================
0 // MENTO LIGHTING - SUNSET SIEGE
0 // ============================================================

0 // Key: Warm sunset from west
0 !MENTO LIGHT "Sunset" TYPE SUN POS {-cam_distance} {tower_top * 2} {half} TGT 0 {tower_top // 2} 0 COLOR #FF9944 INTENSITY 1.0 SHADOWS TRUE

0 // Fill: Cool shadow fill from north
0 !MENTO LIGHT "Shadow" TYPE SUN POS {half} {tower_top * 2} {-cam_distance} TGT 0 {tower_top // 2} 0 COLOR #5588BB INTENSITY 0.25 SHADOWS FALSE

0 // Gate torches
0 !MENTO LIGHT "Torch L" TYPE POINT POS -60 {tower_top} {wall_pos - 30} COLOR #FF8844 INTENSITY 1.2 DECAY 100
0 !MENTO LIGHT "Torch R" TYPE POINT POS 60 {tower_top} {wall_pos - 30} COLOR #FF8844 INTENSITY 1.2 DECAY 100

0 // Keep glow
0 !MENTO LIGHT "Keep" TYPE POINT POS 0 {keep_roof_y // 2} 0 COLOR #FFCC66 INTENSITY 0.4 DECAY {half // 2}

0 // ============================================================
0 // MENTO CAMERA TRACK
0 // ============================================================

0 !MENTO SHOT "Establish" POS {-cam_distance} {tower_top - 80} {cam_distance} TGT 0 {tower_top // 2} 0 LENS 50 DURATION 6
0 !MENTO SHOT "Invaders" POS 0 -50 {wall_pos + 250} TGT 0 -40 {wall_pos} LENS 35 DURATION 5
0 !MENTO SHOT "Gatekeeper" POS 0 -70 {wall_pos + 100} TGT 0 -40 {wall_pos - 60} LENS 60 DURATION 6
0 !MENTO SHOT "Defenders" POS 0 {tower_top - 30} {half} TGT 0 {wall_top_y - 40} {-wall_pos} LENS 70 DURATION 5
0 !MENTO SHOT "Keep" POS {half // 2} {keep_roof_y - 60} {half // 4} TGT 0 {keep_roof_y // 2} 0 LENS 45 DURATION 5
0 !MENTO SHOT "Tactical" POS 0 {tower_top * 5} 0 TGT 0 0 0 LENS 30 DURATION 4
0 !MENTO SHOT "Sunset" POS {-cam_distance // 2} {tower_top - 60} {cam_distance // 2} TGT 0 {tower_top // 2} 0 LENS 85 DURATION 6

0 // ============================================================
0 // GEOMETRY
0 // ============================================================

0 STEP
0 // FLOOR

"""
    content = header + emit_parts(parts) + "\n\n0 NOFILE\n"
    return content, len(parts)


def main():
    configs = [
        ("CASTLE_SMALL.mpd", 32, 3, 6, False, 0),
        ("CASTLE_MEDIUM.mpd", 48, 4, 8, True, 7),
        ("CASTLE_LARGE.mpd", 64, 5, 10, True, 9),
    ]
    
    print("Generating castles v9 (Rich Siege Scene)...\n")
    
    for filename, castle_size, wall_layers, tower_layers, has_keep, keep_layers in configs:
        content, part_count = generate_castle(castle_size, wall_layers, tower_layers,
                                               has_keep, keep_layers)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        size_kb = len(content.encode()) / 1024
        
        print(f"✓ {filename}")
        print(f"  {castle_size}x{castle_size} studs | {tower_layers} layer towers")
        print(f"  {part_count:,} parts | {size_kb:.1f} KB\n")
    
    print("Done!")
    print("- 6+ Defenders on north wall + tower tops")
    print("- 2 Gatekeepers at gate")
    print("- 6+ Invaders outside south gate")
    print("- Props: containers, barrels, lampposts, trees")


if __name__ == "__main__":
    main()
