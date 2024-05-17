import cv2
import numpy as np
import json
from PIL import Image, ImageDraw

# color    = {
#     "Chapati": [244, 164, 96],      # Skin color
#     "White_rice": [255, 255, 255],  # White
#     "Paneer_masala": [255, 165, 0], # Orange
#     "onions": [0, 128, 0],           # Green
#     "Chicken_gravy": [255, 165, 0] # Orange
# }
#color = {"rice":[255,0,255],"vegetable":[255,255,0],"chicken":[0,255,255]}

color = {
    "Chapati": [244, 164, 96],        # Skin color
    "White_rice": [255, 255, 255],    # White
    "Paneer_masala": [255, 165, 0],   # Orange
    "onions": [0, 128, 0],            # Green
    "Chicken_gravy": [255, 165, 0],   # Orange
    "Bindi": [34, 139, 34],           # Forest Green
    "Brinjal_gravy": [128, 0, 128],   # Purple
    "Cabbage": [173, 255, 47],        # Green Yellow
    "Cauliflower": [255, 250, 205],   # Lemon Chiffon
    "Channa_masala": [210, 105, 30],  # Chocolate
    "Chicken": [255, 69, 0],          # Red Orange
    "Chicken_biryani": [255, 215, 0], # Gold
    "Chilli_chutney": [255, 0, 0],    # Red
    "Cocunut_chutney": [240, 255, 240], # Honeydew
    "Cocunut_rice": [245, 255, 250],  # Mint Cream
    "Curd": [255, 255, 240],          # Ivory
    "Curd_rice": [255, 248, 220],     # Cornsilk
    "Dosa": [255, 222, 173],          # Navajo White
    "Egg_gravy": [218, 165, 32],      # Goldenrod
    "Gulab_jamun": [165, 42, 42],     # Brown
    "Idly": [255, 250, 240],          # Floral White
    "Kurma": [255, 228, 181],         # Moccasin
    "Mint_chutney": [152, 251, 152],  # Pale Green
    "Nan": [245, 222, 179],           # Wheat
    "Papad": [255, 239, 213],         # Papaya Whip
    "Parotta": [250, 250, 210],       # Light Goldenrod Yellow
    "Payasam": [255, 228, 225],       # Misty Rose
    "Pongal": [240, 230, 140],        # Khaki
    "Poori": [255, 218, 185],         # Peach Puff
    "Pulav": [240, 255, 240],         # Honeydew
    "Rasam": [255, 69, 0],            # Red Orange
    "Rose_milk": [255, 182, 193],     # Light Pink
    "Salna": [244, 164, 96],          # Skin Color
    "Sambar": [255, 140, 0],          # Dark Orange
    "Sweet_pongal": [255, 235, 205],  # Blanched Almond
    "Tamarind_rice": [222, 184, 135], # Burly Wood
    "Vada": [218, 165, 32],           # Goldenrod
    "Veg_biryani": [144, 238, 144],   # Light Green
    "bajji": [255, 160, 122],         # Light Salmon
    "beans": [34, 139, 34],           # Forest Green
    "binndi": [34, 139, 34],          # Forest Green
    "egg": [255, 255, 240],           # Ivory
    "fish_curry": [255, 99, 71],      # Tomato
    "fish_fry": [210, 105, 30],       # Chocolate
    "kesari": [255, 127, 80],         # Coral
    "kuli_paniyaram": [245, 245, 220],# Beige
    "ladoo": [255, 215, 0],           # Gold
    "lemon_rice": [255, 250, 205],    # Lemon Chiffon
    "potato": [210, 180, 140],        # Tan
    "prawn_fry": [255, 99, 71],       # Tomato
    "prawn_gravy": [255, 69, 0],      # Red Orange
    "rasa_malai": [255, 245, 238]     # Seashell
}


def polygons_to_mask(img_shape, polygons):
    mask = np.zeros(img_shape, dtype=np.uint8)
    mask = Image.fromarray(mask)
    xy = list(map(tuple, polygons))
    ImageDraw.Draw(mask).polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)

    return mask

def mask2box(mask):
    index = np.argwhere(mask == 1)
    rows = index[:, 0]
    clos = index[:, 1]
    left_top_r = np.min(rows)
    left_top_c = np.min(clos)
    right_bottom_r = np.max(rows)
    right_bottom_c = np.max(clos)

    return [left_top_c, left_top_r, right_bottom_c, right_bottom_r]


def get_bbox(points, h, w):
    polygons = points
    mask = polygons_to_mask([h,w], polygons)

    return mask2box(mask)

def get_mask(img, json_path):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        mask = np.zeros((img.shape[0], img.shape[1], 3), dtype=int)
        for shape in data['shapes']:
            label = shape['label']
            if (label == "plate"):
                continue
            points = shape['points']
            bbox = get_bbox(points, img.shape[0], img.shape[1])
            points = np.array(points, dtype=np.float32)
            points = points.reshape((-1, 1, 2))

            for i in range(bbox[0], bbox[2] + 1):
                for j in range(bbox[1], bbox[3] + 1):
                    if (cv2.pointPolygonTest(points, (i, j), False) >= 0):
                        mask[j][i] = color[label]

        cv2.imwrite("output/mask.png", mask)

