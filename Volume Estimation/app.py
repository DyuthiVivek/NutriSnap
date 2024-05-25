from flask import Flask, render_template, request
import main, nutrient_info

app = Flask(__name__)

UPLOAD_FOLDER = './input'
INPUT_FOLDER = './input'

@app.route('/', methods=['GET', 'POST'])
def upload_video():
    message = ""
    info = {}
    total = {}

    if request.method == 'POST':
        image_file = request.files['image-upload']

        if image_file:
            filename = image_file.filename
            allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
            name, ext = filename.split('.')

            if ext in allowed_extensions:
                image_path = f'{UPLOAD_FOLDER}/test.jpg'
                output_path = f'{INPUT_FOLDER}/test.json'
                image_file.save(image_path)
                message = f'Image {filename} uploaded successfully!'
                volumes = main._main(image_path, output_path)

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
            else:
                message = 'Invalid image format. Allowed formats: PNG, JPG, JPEG, GIF'
        else:
            message = 'No image file selected.'

    return render_template('index.html', message=message, info=info, total=total)

if __name__ == '__main__':
  app.run(debug=True)