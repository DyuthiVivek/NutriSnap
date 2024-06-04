from convert_to_labelme import convert_image_to_json
from remove_alpha_channel import remove_alpha
from demo import main
import nutrient_info

def _main(input_image_path, output_path):
    remove_alpha(input_image_path)
    convert_image_to_json(input_image_path, output_path)
    volumes = main()
    return volumes[0]

def calc_total(volumes):
    info = {}
    total = {}

    for item in volumes:
        weight = nutrient_info.food_info[item]["density"] * volumes[item]

        item_info = {
            "weight" : weight,
            "calories": nutrient_info.food_info[item]["calories"] * weight,
            "protein": nutrient_info.food_info[item]["protein"] * weight,
            "carbohydrates": nutrient_info.food_info[item]["carbohydrates"] * weight,
            "fat": nutrient_info.food_info[item]["fat"] * weight,
            "fiber": nutrient_info.food_info[item]["fiber"] * weight
        }

        formatted_item = item.replace("_", " ").title()
        info[formatted_item] = item_info

        total = {
            "calories" : sum(info[item]["calories"] for item in info),
            "protein" : sum(info[item]["protein"] for item in info),
            "carbohydrates" : sum(info[item]["carbohydrates"] for item in info),
            "fat" : sum(info[item]["fat"] for item in info),
            "fiber" : sum(info[item]["fiber"] for item in info),
        }

        major_nutrients = total["carbohydrates"] + total["protein"] + total["fat"] + total["fiber"]
        total["other"] = sum(info[item]["weight"] for item in info) - major_nutrients
    return total, info
