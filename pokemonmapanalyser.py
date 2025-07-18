from PIL import Image
import numpy as np

# === CONFIGURATION ===
TILE_SIZE = 16
TOLERANCE = 0 # Ajuste si besoin
TILESET_PATH = "E:/Python/Pokemon Emeraude/assets/tilesets/outdoors.png"
MAP_PATH = "C:/Users/c.magloire/Desktop/route_101.png"
OUTPUT_PATH = "C:/Users/c.magloire/Desktop/map_output.txt"

# === FONCTION DE COMPARAISON SOUPLE ===
def compare_tiles_soft(tile1, tile2, tolerance):
    diff = np.abs(tile1.astype(int) - tile2.astype(int))
    return np.mean(diff) <= tolerance

# === CHARGEMENT ET CONVERSION ===
tileset_img = Image.open(TILESET_PATH).convert("RGB")
map_img = Image.open(MAP_PATH).convert("RGB")

tileset_np = np.array(tileset_img)
map_np = np.array(map_img)

tileset_width, tileset_height = tileset_img.size
map_width, map_height = map_img.size

tileset_tiles_x = tileset_width // TILE_SIZE
tileset_tiles_y = tileset_height // TILE_SIZE
map_tiles_x = map_width // TILE_SIZE
map_tiles_y = map_height // TILE_SIZE

# === COMPARAISON ET GÉNÉRATION ===
output_lines = []

for y in range(map_tiles_y):
    row_data = []
    for x in range(map_tiles_x):
        tile = map_np[y*TILE_SIZE:(y+1)*TILE_SIZE, x*TILE_SIZE:(x+1)*TILE_SIZE]

        match = None
        for ty in range(tileset_tiles_y):
            for tx in range(tileset_tiles_x):
                candidate = tileset_np[ty*TILE_SIZE:(ty+1)*TILE_SIZE, tx*TILE_SIZE:(tx+1)*TILE_SIZE]
                if compare_tiles_soft(tile, candidate, TOLERANCE):
                    match = (tx, ty)
                    break
            if match:
                break

        if match:
            coord_str = f"0,{match[0]},{match[1]},0,0"
        else:
            coord_str = "0,0,0,0,0"
        row_data.append(coord_str)

    output_lines.append(";".join(row_data))  # Ne pas ajouter de ; final

# === SAUVEGARDE DU FICHIER ===
with open(OUTPUT_PATH, "w") as f:
    for line in output_lines:
        f.write(line + "\n")

print(f"Fichier généré sans ';' final : {OUTPUT_PATH}")
